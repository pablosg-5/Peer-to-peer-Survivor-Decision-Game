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
            peer_decision = recv_data(sock)
            if peer_decision:
                if "decision" in peer_decision:
                    game.register_decision(peer_decision["player"], peer_decision["decision"])
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

def start_p2p(host, port,username, peers):
    exit_flag = threading.Event()
    connections = []
    game = Game(username, [p["username"] for p in peers]) 
    retry_event = threading.Event()
    peer_retry_data = {"retry": None, "start_new_game": False}
    lock = threading.Lock()

    # Hilo para aceptar conexiones
    def accept_connections():
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen(2)
        print(f"\n🕑 Waiting for connections on {host}:{port}...")
        
        connections_made = 0
        while connections_made < 2 and not exit_flag.is_set():
            try:
                conn, addr = server.accept()
                print(f"✅ Connection accepted from {addr}")
                connections.append(conn)
                connections_made += 1
            except:
                break
        server.close()

    # Hilo para conectar a peers
    def connect_to_peers():
        for peer in peers:
            retries = 0
            while retries < 3 and not exit_flag.is_set():
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(10)
                    sock.connect((peer["ip"], peer["port"]))
                    print(f"\n✅ Connected to {peer['username']}")
                    connections.append(sock)
                    break
                except Exception as e:
                    print(f"⚠️ Retrying connection to {peer['username']}... ({e})")
                    retries += 1
                    time.sleep(2)

    # Iniciar conexiones
    acceptor_thread = threading.Thread(target=accept_connections, daemon=True)
    connector_thread = threading.Thread(target=connect_to_peers, daemon=True)
    acceptor_thread.start()
    connector_thread.start()
    
    # Esperar conexiones
    start_time = time.time()
    while len(connections) < 2 and not exit_flag.is_set():
        if time.time() - start_time > 30:
            print("❌ Connection timeout")
            exit_flag.set()
            return
        time.sleep(0.1)

    # Hilos receptores
    receiver_threads = []
    for conn in connections:
        thread = threading.Thread(
            target=handle_peer_connection,
            args=(conn, game, retry_event, peer_retry_data, exit_flag),
            daemon=True
        )
        thread.start()
        receiver_threads.append(thread)

    # Bucle principal del juego
    try:
        while not exit_flag.is_set():
            scenario = game.get_scenario()
            
            print("\n" + "=" * 50)
            print(scenario["scenario"])
            print("=" * 50)
            time.sleep(2)

            if "end_game" in scenario["choices"]:
                game.game_over = True

            if game.game_over:
                print("\nGAME OVER!")
                time.sleep(1)
                print(game.game_result)
                print("=" * 50)

                # Gestión de reinicio
                retry = None
                while retry not in ["y", "n"]:
                    retry = input("\nRestart? (y/n): ").lower().strip()
                    if retry not in ["y", "n"]:
                        print("Invalid option!")

                # Enviar decisión a ambos peers
                for conn in connections:
                    send_data(conn, {"retry": retry})
                print("Waiting for other players...")
                
                retry_event.wait(timeout=15)
                peer_retries = [peer_retry_data["retry"] for _ in range(2)]  # Para 2 peers
                retry_event.clear()

                if retry == "y" and all(r == "y" for r in peer_retries):
                    print("\nRestarting game...")
                    game.full_reset()
                    peer_retry_data.update({"retry": None, "start_new_game": False})
                    
                    # Reenviar señal de reinicio
                    for conn in connections:
                        send_data(conn, {"start_new_game": True})
                    
                    # Esperar confirmación
                    start_wait = time.time()
                    while not peer_retry_data["start_new_game"] and time.time() - start_wait < 10:
                        time.sleep(0.1)
                    continue
                else:
                    print("\nGame over")
                    exit_flag.set()
                    return

            # Obtener decisión local
            while True:
                try:
                    choice = int(input("\nYour choice (1/2): "))
                    if choice in [1, 2]:
                        with lock:
                            game.player_decision = choice
                        for conn in connections:
                            send_data(conn, {"decision": choice})
                        break
                    print("Invalid option! Only 1 or 2")
                except ValueError:
                    print("Invalid input! Only numbers")

            # Esperar 2 decisiones
            print("\nWaiting for partners...")
            start_wait = time.time()
            while len(game.received_decisions) < 2 and not exit_flag.is_set():
                if time.time() - start_wait > 30:
                    print("Time expired!")
                    game.game_over = True
                    break
                time.sleep(0.1)

            # Procesar decisiones
            print(f"\nDecisions received: {game.received_decisions}")
            game.process_decisions()
            game.reset_decisions()
            input("\nPress Enter to continue...")

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        exit_flag.set()
        for conn in connections:
            conn.close()