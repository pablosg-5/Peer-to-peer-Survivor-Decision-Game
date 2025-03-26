import socket
import json
import threading
import time
import random
from game import Game

# ==============================================
# Network Protocol Utilities
# ==============================================

bot_players = set()  # Bot player list


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
    sock.settimeout(2.0)
    while not exit_flag.is_set():
        try:
            data = recv_data(sock)
            if data: 
                if "decision" in data:
                    with lock:
                        game.register_decision(data["player"], data["decision"])
                        if "bot_decisions" in data:
                            for bot, bot_decision in data["bot_decisions"].items():
                                game.register_decision(bot, bot_decision)
                elif "retry" in data:
                    with lock:
                        peer_retry_data[data["player"]] = data["retry"]
                    retry_event.set()
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

    def wait_for_decisions(game, timeout=30):
        # Wait for player decisions with timeout
        # if some player is missing, the game will continue with bots.
        
        player_to_wait = 2 - len(bot_players)

        if (len(bot_players) == 2):
            missing_players = [
                p for p in game.peer_usernames if p not in game.received_decisions]
            for player in missing_players:
                bot_choice = random.choice([1, 2])
                print(f"🤖 Bot ({player}) chooses option {bot_choice}")
                time.sleep(1)
                game.register_decision(player, bot_choice)
        else:
            print("\n⏳ Waiting for other players' decisions...")
            start_wait = time.time()
            while len(game.received_decisions) < player_to_wait and not exit_flag.is_set():
                if time.time() - start_wait > timeout:
                    print("\n⌛ Decision timeout! Checking missing players...\n")
                    time.sleep(1)
                    missing_players = [
                        p for p in game.peer_usernames if p not in game.received_decisions]

                    for player in missing_players:
                        if player not in bot_players:
                            print(f"🤖 {player} is eliminated of the game for desconection")
                            bot_players.add(player)
                    time.sleep(2)
                    break
                time.sleep(0.1)

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

                if len(bot_players) == 0:
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
                else:
                    if retry == "y":
                        print("\n🤖 All players are bots! Synchronizing restart...")
                        game.full_reset()
                        peer_retry_data.clear()
                        game_reset_event.clear()
                        bot_players.add(game.peer_usernames[0])
                        bot_players.add(game.peer_usernames[1])
                        print("\n🔥 NEW GAME STARTED SUCCESSFULLY!")
                        time.sleep(2)
                        continue
                    else:
                        print("\nClosing game...")
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
                                send_data(conn, {"decision": choice, "player": username})
                        break
                    print("Invalid option! Only 1 or 2")
                except ValueError:
                    print("Invalid input! Numbers only")

            # ==============================================
            # Decision Synchronization
            # ==============================================
            wait_for_decisions(game)  # wait for other players decisions
            if len(game.received_decisions) < 2:
                wait_for_decisions(game) # if only get the bots, repeteat one time for the decision of the bots

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
