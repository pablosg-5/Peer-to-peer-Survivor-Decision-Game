import socket
import json
import threading
import time
from game import Game


def recv_data(sock):
    # Receives a JSON message from the socket.
    try:
        raw_len = sock.recv(4)
        if not raw_len:
            return None
        msg_len = int.from_bytes(raw_len, byteorder='big')
        data = sock.recv(msg_len).decode('utf-8')
        return json.loads(data)
    except (ConnectionResetError, json.JSONDecodeError, OSError):
        return None


def send_data(sock, message):
    # Sends a JSON message through the socket.
    try:
        data = json.dumps(message).encode('utf-8')
        msg_len = len(data).to_bytes(4, byteorder='big')
        sock.sendall(msg_len + data)
        return True
    except (BrokenPipeError, OSError):
        return False


def handle_peer_connection(sock, game, retry_event, peer_retry_data, exit_flag):
    # Handles receiving decisions from the other player.
    while not exit_flag.is_set():
        peer_decision = recv_data(sock)
        if peer_decision:
            if "decision" in peer_decision:
                game.other_player_decision = peer_decision["decision"]
            elif "retry" in peer_decision:
                peer_retry_data["retry"] = peer_decision["retry"]
                retry_event.set()  # Notify that a restart response was received
            elif "start_new_game" in peer_decision:
                # Synchronization signal to start a new game
                peer_retry_data["start_new_game"] = True
                retry_event.set()
        time.sleep(0.1)


def start_p2p(host, port, peer_host=None, peer_port=None):
    exit_flag = threading.Event()
    
    while True:  # Main loop for game restarts
        game = Game()
        connection = None
        lock = threading.Lock()
        retry_event = threading.Event()  # Used to signal when a retry response is received
        peer_retry_data = {"retry": None, "start_new_game": False}  # Shared data between threads

        # Connection setup
        def accept_connection():
            nonlocal connection
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((host, port))
            server.listen(1)
            print(f"Waiting for a connection at {host}:{port}...")
            conn, addr = server.accept()
            with lock:
                connection = conn
            print(f"Connected with {addr}")
            server.close()

        def connect_to_peer():
            nonlocal connection
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((peer_host, peer_port))
                with lock:
                    connection = sock
                print(f"Connected to {peer_host}:{peer_port}")
            except Exception as e:
                print(f"Connection error: {str(e)}")

        # Establish connection
        if peer_host and peer_port:
            threading.Thread(target=connect_to_peer, daemon=True).start()

        accept_thread = threading.Thread(target=accept_connection, daemon=True)
        accept_thread.start()
        accept_thread.join(timeout=10)

        if not connection:
            print("Connection failed")
            return

        # Thread to receive decisions
        receiver_thread = threading.Thread(
            target=handle_peer_connection,
            args=(connection, game, retry_event, peer_retry_data, exit_flag),
            daemon=True
        )
        receiver_thread.start()

        # Main game loop
        try:
            while not game.game_over:
                scenario = game.get_scenario()

                print("\n" + "=" * 50)
                print(scenario["scenario"])
                print("=" * 50)

                if "end_game" in scenario["choices"]:
                    game.game_over = True

                if game.game_over:
                    # Handle end of game
                    print("\n")
                    print("GAME OVER!")
                    print(game.game_result)
                    print("=" * 50)

                    # Restart management
                    retry = None
                    while retry not in ["y", "n"]:
                        retry = input("\nRestart? (y/n): ").lower().strip()
                        if retry not in ["y", "n"]:
                            print("Invalid option!")
                    
                    # Send our decision first
                    send_data(connection, {"retry": retry})
                    print("Waiting for the other player's response...")

                    # Wait for confirmation with timeout
                    retry_event.wait(timeout=15)  # Wait for signal or timeout
                    peer_retry = peer_retry_data["retry"]
                    retry_event.clear()  # Clear for future events

                    # Decide on restart
                    print(f"DEBUG: The other player chose: {peer_retry}")
                    if retry == "y" and peer_retry == "y":
                        print("\nRestarting...")
                        # Send signal that we are ready to start
                        send_data(connection, {"start_new_game": True})
                        peer_retry_data["start_new_game"] = False
                        print("Synchronizing restart...")

                        # Wait for the other node to be ready
                        start_wait = time.time()
                        while not peer_retry_data["start_new_game"]:
                            if time.time() - start_wait > 10:
                                print("Synchronization error, but attempting to continue...")
                                break
                            time.sleep(0.1)
                            # Resend in case it wasn't received
                            if time.time() - start_wait > 5 and not peer_retry_data["start_new_game"]:
                                send_data(connection, {"start_new_game": True})

                        # Reset game and clear data
                        game.reset_game(True)
                        continue
                    else:
                        print("\nAt least one of the two players does not want to play again. Game over")
                        exit_flag.set()  # Signal to stop receiver thread
                        connection.close()
                        return 

                # Get local player's decision
                while True:
                    try:
                        choice = int(input("\nYour choice (1/2): "))
                        if choice in [1, 2]:
                            with lock:
                                game.player_decision = choice
                            send_data(connection, {"decision": choice})
                            break
                        print("Invalid option! Only 1 or 2")
                    except ValueError:
                        print("Invalid input! Only numbers")

                # Wait for remote player's decision
                print("\nWaiting for partner...")
                start_wait = time.time()
                while game.other_player_decision is None:
                    if time.time() - start_wait > 30:
                        print("Time expired!")
                        game.game_over = True
                        break
                    time.sleep(0.1)

                # Process decisions
                print(f"\nPartner chose: {game.other_player_decision}")
                game.process_decisions()
                game.reset_decisions()
                input("\nPress Enter to continue...")

        except Exception as e:
            print(f"Game error: {str(e)}")
        finally:
            if connection:
                try:
                    connection.close()
                except:
                    pass
            time.sleep(1)
