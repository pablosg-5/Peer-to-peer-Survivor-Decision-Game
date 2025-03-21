import socket
import json
import threading
import time
from game import Game


def recv_data(sock):
    try:
        raw_len = sock.recv(4)
        if not raw_len:
            return None
        msg_len = int.from_bytes(raw_len, byteorder='big')
        data = sock.recv(msg_len).decode('utf-8')
        return json.loads(data)
    except (ConnectionResetError, json.JSONDecodeError, OSError, socket.timeout):
        return None


def send_data(sock, message):
    try:
        data = json.dumps(message).encode('utf-8')
        msg_len = len(data).to_bytes(4, byteorder='big')
        sock.sendall(msg_len + data)
        return True
    except (BrokenPipeError, OSError):
        return False


def handle_peer_connection(sock, game, retry_event, peer_retry_data, exit_flag):
    sock.settimeout(2.0)   # Timeout to prevent blocking
    while not exit_flag.is_set():
        try:
            peer_decision = recv_data(sock)
            if peer_decision:
                if "decision" in peer_decision:
                    game.other_player_decision = peer_decision["decision"]
                elif "retry" in peer_decision:
                    peer_retry_data["retry"] = peer_decision["retry"]
                    retry_event.set()
                elif "start_new_game" in peer_decision:
                    peer_retry_data["start_new_game"] = True
                    retry_event.set()
        except socket.timeout:
            continue
        except:
            break
        time.sleep(0.1)


def start_p2p(host, port, peer_host, peer_port, peer_username):
    exit_flag = threading.Event()
    connection = None
    game = Game(peer_username)
    retry_event = threading.Event()
    peer_retry_data = {"retry": None, "start_new_game": False}
    lock = threading.Lock()

    def establish_connection():
        nonlocal connection

        def accept_connection():
            nonlocal connection
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                server.bind((host, port))
                server.listen(1)
                server.settimeout(20)
                conn, _ = server.accept()
                with lock:
                    connection = conn
                print(f"\n✅ Connection accepted from peer")
            except Exception as e:
                print(f"❌ Accept error: {e}")
            finally:
                server.close()

        def connect_to_peer():
            nonlocal connection
            retries = 0
            while retries < 3 and not exit_flag.is_set():
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(10)
                    sock.connect((peer_host, peer_port))
                    with lock:
                        connection = sock
                    print(f"\n✅ Connected to {peer_username}")
                    return
                except Exception as e:
                    print(f"⚠️ Connection error: {e}")
                    retries += 1
                    time.sleep(2)

        acceptor = threading.Thread(target=accept_connection, daemon=True)
        connector = threading.Thread(target=connect_to_peer, daemon=True)
        acceptor.start()
        connector.start()
        acceptor.join(timeout=15)
        connector.join(timeout=15)

    # Establish initial connection
    establish_connection()

    if not connection:
        print("❌ Critical: Connection failed")
        return

    # Configure timeout and start the receiver thread
    connection.settimeout(5.0)
    receiver_thread = threading.Thread(
        target=handle_peer_connection,
        args=(connection, game, retry_event, peer_retry_data, exit_flag),
        daemon=True
    )
    receiver_thread.start()

    # Main game loop
    try:
        while not exit_flag.is_set():
            scenario = game.get_scenario()
            print("\n" + "=" * 50)
            print(scenario["scenario"])
            print("=" * 50)

            if "end_game" in scenario["choices"]:
                game.game_over = True

            if game.game_over:
                print("\nGAME OVER!\n" + game.game_result)
                retry = input("\nRestart? (y/n): ").lower().strip()
                while retry not in ["y", "n"]:
                    retry = input("Invalid option! (y/n): ")

                send_data(connection, {"retry": retry})
                print("Waiting for peer...")
                retry_event.wait(timeout=15)
                peer_retry = peer_retry_data["retry"]
                retry_event.clear()

                if retry == "y" and peer_retry == "y":
                    print("\nRestarting game...")

                    # Reset all conexion
                    exit_flag.set()
                    receiver_thread.join()
                    if connection:
                        connection.close()
                    exit_flag.clear()
                    game.full_reset()
                    peer_retry_data.update(
                        {"retry": None, "start_new_game": False})

                    establish_connection()
                    if not connection:
                        print("❌ Failed to reconnect")
                        return

                    receiver_thread = threading.Thread(
                        target=handle_peer_connection,
                        args=(connection, game, retry_event,
                              peer_retry_data, exit_flag),
                        daemon=True
                    )
                    receiver_thread.start()
                    continue
                else:
                    print(
                        "\nAt least one of the two players does not want to play again. Game over\n")
                    exit_flag.set()
                    return

            while True:
                try:
                    choice = int(input("\nYour choice (1/2): "))
                    if choice in [1, 2]:
                        with lock:
                            game.player_decision = choice
                        send_data(connection, {"decision": choice})
                        break
                    print("Invalid option!")
                except ValueError:
                    print("Numbers only!")

            # Wait for the other player decision
            print("\nWaiting for partner...")
            start_wait = time.time()
            while game.other_player_decision is None and not exit_flag.is_set():
                if time.time() - start_wait > 30:
                    print("Time expired!")
                    game.game_over = True
                    break
                time.sleep(0.1)

            # Process decisions
            print(f"\n{game.peer_username} chose: {game.other_player_decision}")
            game.process_decisions()
            game.reset_decisions()

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        exit_flag.set()
        if connection:
            connection.close()
