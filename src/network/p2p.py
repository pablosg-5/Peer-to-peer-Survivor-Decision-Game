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
    sock.settimeout(2.0)
    while not exit_flag.is_set():
        try:
            data = recv_data(sock)
            if data:
                if "decision" in data:
                    game.register_decision(data["player"], data["decision"])
                elif "retry" in data:
                    peer_retry_data[data["player"]] = data["retry"]  # Track by username
                    retry_event.set()
                elif "start_new_game" in data:
                    peer_retry_data["start_new_game"] = True
                    retry_event.set()
        except socket.timeout:
            continue
        except:
            break
        time.sleep(0.1)

def start_p2p(host, port, username, peers):
    exit_flag = threading.Event()
    connections = []
    game = Game(username, [p["username"] for p in peers])
    retry_event = threading.Event()
    peer_retry_data = {}  # Now tracks responses by username
    lock = threading.Lock()

    # ==============================================
    # Connection handling (improved for 3 players)
    # ==============================================
    def accept_connections():
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen(2)
        print(f"\n🕑 Waiting for incoming connections on {host}:{port}...")
        
        try:
            while len(connections) < 2 and not exit_flag.is_set():
                conn, addr = server.accept()
                print(f"✅ Connection accepted from {addr[0]}:{addr[1]}")
                connections.append(conn)
        finally:
            server.close()

    def connect_to_peers():
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
                    print(f"⚠️ Failed to connect to {peer['username']}: {str(e)}")
                    retries += 1
                    time.sleep(2)

    # ==============================================
    # Game loop with proper 3-player synchronization
    # ==============================================
    try:
        # Establish connections
        acceptor_thread = threading.Thread(target=accept_connections, daemon=True)
        connector_thread = threading.Thread(target=connect_to_peers, daemon=True)
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

        # Start receiver threads
        receiver_threads = []
        for conn in connections:
            thread = threading.Thread(
                target=handle_peer_connection,
                args=(conn, game, retry_event, peer_retry_data, exit_flag),
                daemon=True
            )
            thread.start()
            receiver_threads.append(thread)

        # Main game loop
        while not exit_flag.is_set():
            scenario = game.get_scenario()
            
            print("\n" + "=" * 50)
            print(scenario["scenario"])
            print("=" * 50)
            time.sleep(2)

            if "end_game" in scenario["choices"]:
                game.game_over = True

            if game.game_over:
                print("\n💀 GAME OVER!")
                time.sleep(1)
                print(game.game_result)
                print("=" * 50)

                # Restart logic for 3 players
                retry = None
                while retry not in ["y", "n"]:
                    retry = input("\nPlay again? (y/n): ").lower().strip()
                    if retry not in ["y", "n"]:
                        print("Invalid option!")

                # Send decision to both peers
                for conn in connections:
                    send_data(conn, {
                        "retry": retry,
                        "player": username  # Include username in restart message
                    })
                
                print("\n🕒 Waiting for other players' responses...")
                
                # Wait for both peers to respond
                start_wait = time.time()
                required_peers = [p["username"] for p in peers]
                while not exit_flag.is_set():
                    received_peers = [p for p in required_peers if p in peer_retry_data]
                    if len(received_peers) == 2:
                        break
                    if time.time() - start_wait > 15:
                        print("⌛ Timeout waiting for players")
                        break
                    time.sleep(0.1)

                # Check responses from both peers
                peer_responses = [peer_retry_data.get(p, "n") for p in required_peers]
                if retry == "y" and all(r == "y" for r in peer_responses):
                    print("\n🔄 Restarting game with all players...")
                    
                    # Full reset with reconnection
                    game.full_reset()
                    exit_flag.set()
                    for conn in connections:
                        conn.close()
                    exit_flag.clear()
                    start_p2p(host, port, username, peers)  # Reinitialize
                    return
                else:
                    print("\n❌ Not all players want to continue")
                    exit_flag.set()
                    return

            # Decision making
            while True:
                try:
                    choice = int(input("\nYour choice (1/2): "))
                    if choice in [1, 2]:
                        with lock:
                            game.player_decision = choice
                        # Send to all peers with username
                        for conn in connections:
                            send_data(conn, {
                                "decision": choice,
                                "player": username
                            })
                        break
                    print("Invalid option! Only 1 or 2")
                except ValueError:
                    print("Invalid input! Numbers only")

            # Wait for 2 decisions
            print("\n⏳ Waiting for other players' decisions...")
            start_wait = time.time()
            while len(game.received_decisions) < 2 and not exit_flag.is_set():
                if time.time() - start_wait > 30:
                    print("⌛ Decision timeout!")
                    game.game_over = True
                    break
                time.sleep(0.1)

            # Process decisions
            if not exit_flag.is_set():
                game.process_decisions()
                game.reset_decisions()
                input("\nPress Enter to continue...")

    except Exception as e:
        print(f"\n⚠️ Critical error: {str(e)}")
    finally:
        exit_flag.set()
        for conn in connections:
            try:
                conn.close()
            except:
                pass