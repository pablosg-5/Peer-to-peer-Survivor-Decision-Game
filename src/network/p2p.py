import socket
import json
import threading
import time
from game import Game

# ==============================================
# Network Protocol Utilities
# ==============================================


def recv_data(sock):
    try:
        # Read message length header
        raw_len = sock.recv(4)
        if not raw_len:
            return None
        msg_len = int.from_bytes(raw_len, byteorder='big')

        # Read actual message data
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

# ==============================================
# Peer Connection Handler
# ==============================================


def handle_peer_connection(sock, game, retry_event, peer_retry_data, game_reset_event, exit_flag, lock, peers):
    """
    Thread target for handling incoming messages from a peer connection.
    Handles three types of messages:
    1. Player decisions (choice 1/2)
    2. Retry requests after game over
    3. New game synchronization messages
    """
    sock.settimeout(2.0)
    while not exit_flag.is_set():
        try:
            data = recv_data(sock)
            if data:
                # Handle player decision messages
                if "decision" in data:
                    with lock:
                        game.register_decision(
                            data["player"], data["decision"])

                # Handle game retry requests
                elif "retry" in data:
                    with lock:
                        peer_retry_data[data["player"]] = data["retry"]
                    retry_event.set()

                # Handle new game synchronization
                elif "start_new_game" in data:
                    with lock:
                        if data["player"] not in peer_retry_data:
                            peer_retry_data[data["player"]] = True
                            print(
                                f"\n🔄 Reset confirmation received from {data['player']}")
                            if len(peer_retry_data) == len(peers):
                                game.full_reset()
                                game_reset_event.set()
        except socket.timeout:
            continue
        except:
            break
        time.sleep(0.1)

# ==============================================
# P2P Game Server Core
# ==============================================


def start_p2p(host, port, username, peers):
    exit_flag = threading.Event()
    connections = []
    game = Game(username, [p["username"] for p in peers])
    retry_event = threading.Event()
    game_reset_event = threading.Event()
    peer_retry_data = {}
    lock = threading.Lock()

    # ==============================================
    # Connection Setup
    # ==============================================
    def accept_connections():
        # Listen for incoming peer connections
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen(2)
        try:
            while len(connections) < 2 and not exit_flag.is_set():
                conn, addr = server.accept()
                connections.append(conn)
        finally:
            server.close()

    def connect_to_peers():
        # Establish outgoing connections to known peers
        for peer in peers:
            retries = 0
            while retries < 3 and not exit_flag.is_set():
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(10)
                    sock.connect((peer["ip"], peer["port"]))
                    print(f"\n✅ Successfully connected to {peer['username']}")
                    connections.append(sock)
                    break
                except Exception as e:
                    print(
                        f"⚠️ Failed to connect to {peer['username']}: {str(e)}")
                    retries += 1
                    time.sleep(2)

    try:
        # ==============================================
        # Network Initialization
        # ==============================================
        # Start connection threads
        acceptor_thread = threading.Thread(
            target=accept_connections, daemon=True)
        connector_thread = threading.Thread(
            target=connect_to_peers, daemon=True)
        acceptor_thread.start()
        connector_thread.start()

        # Wait for connections with timeout
        start_time = time.time()
        while len(connections) < 2 and not exit_flag.is_set():
            if time.time() - start_time > 30:
                print("❌ Connection timeout")
                exit_flag.set()
                return
            time.sleep(0.1)

        # ==============================================
        # Receiver Threads Setup
        # ==============================================
        receiver_threads = []
        for conn in connections:
            thread = threading.Thread(
                target=handle_peer_connection,
                args=(conn, game, retry_event, peer_retry_data,
                      game_reset_event, exit_flag, lock, peers),
                daemon=True
            )
            thread.start()
            receiver_threads.append(thread)

        time.sleep(3)  # Pause for better readability

        # ==============================================
        # Main Game Loop
        # ==============================================
        while not exit_flag.is_set():
            # Display current game scenario
            scenario = game.get_scenario()

            print("\n" + "=" * 50)
            print(scenario["scenario"])
            print("=" * 50)
            time.sleep(2)

            # Check for game over condition
            if "end_game" in scenario["choices"]:
                game.game_over = True

            if game.game_over:
                # Game over display
                print("\n💀 GAME OVER!")
                print(game.game_result)
                print("=" * 50)

                # Retry logic
                retry = None
                while retry not in ["y", "n"]:
                    retry = input("\nPlay again? (y/n): ").lower().strip()
                    if retry not in ["y", "n"]:
                        print("Invalid option!")

                # Broadcast retry decision
                for conn in connections:
                    send_data(conn, {"retry": retry, "player": username})

                print("\n🕒 Waiting for other players' responses...")
                start_wait = time.time()
                required_peers = [p["username"] for p in peers]

                # Wait for peer responses with timeout
                while not exit_flag.is_set():
                    with lock:
                        received = all(
                            p in peer_retry_data for p in required_peers)
                    if received or (time.time() - start_wait > 25):
                        break
                    time.sleep(0.1)

                # Handle restart or exit
                if retry == "y" and all(peer_retry_data.get(p, "n") == "y" for p in required_peers):
                    print("\n🔄 All players agreed! Synchronizing restart...")
                    game.full_reset()
                    peer_retry_data.clear()
                    game_reset_event.clear()
                    print("\n🔥 NEW GAME STARTED SUCCESSFULLY!")
                    time.sleep(2)
                    continue
                else:
                    print("\n❌ Not all players want to continue")
                    exit_flag.set()
                    return

            # ==============================================
            # Player Decision Handling
            # ==============================================
            while not game.game_over and not exit_flag.is_set():
                try:
                    choice = int(input("\nYour choice (1/2): "))
                    if choice in [1, 2]:
                        with lock:
                            game.player_decision = choice
                        # Broadcast decision to peers
                        for conn in connections:
                            send_data(
                                conn, {"decision": choice, "player": username})
                        break
                    print("Invalid option! Only 1 or 2")
                except ValueError:
                    print("Invalid input! Numbers only")

            # ==============================================
            # Decision Synchronization
            # ==============================================
            print("\n⏳ Waiting for other players' decisions...")
            start_wait = time.time()
            while len(game.received_decisions) < 2 and not exit_flag.is_set():
                if time.time() - start_wait > 30:
                    print("\n⌛ Decision timeout! Closing game...")
                    exit_flag.set()
                    return
                time.sleep(0.1)

            # Process decisions if synchronization successful
            if not exit_flag.is_set():
                with lock:

                    print("\n" + "=" * 50)
                    print("💬 Decisions of the players:")
                    print(f"👉 {game.username}: Option:{game.player_decision}")
                    for player, decision in game.received_decisions.items():
                        print(f"👉 {player}: Option:{decision}")
                    print("=" * 50 + "\n")
                    time.sleep(2)
                    game.process_decisions()
                    game.reset_decisions()

    except Exception as e:
        print(f"\n⚠️ Critical error: {str(e)}")
    finally:
        # Cleanup resources
        exit_flag.set()
        for conn in connections:
            try:
                conn.close()
            except:
                pass
