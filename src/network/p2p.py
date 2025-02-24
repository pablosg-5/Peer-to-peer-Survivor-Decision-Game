import socket
import json
import threading
import time
from game import Game


def recv_all(sock):
    """Recibe datos con prefijo de longitud de forma confiable"""
    try:
        raw_len = b""
        while len(raw_len) < 4:
            chunk = sock.recv(4 - len(raw_len))
            if not chunk:
                return None
            raw_len += chunk

        msg_len = int.from_bytes(raw_len, byteorder='big')

        data = b""
        while len(data) < msg_len:
            packet = sock.recv(min(4096, msg_len - len(data)))
            if not packet:
                return None
            data += packet

        return data.decode('utf-8')
    except (ConnectionResetError, ConnectionAbortedError, OSError):
        return None


def start_p2p(host, port, peer_host=None, peer_port=None):
    game = Game()
    connection = None
    lock = threading.Lock()
    sync_active = True
    scenario_processed = False

    def accept_connections():
        nonlocal connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(1)
        print(f"Escuchando en {host}:{port}")
        conn, addr = sock.accept()
        with lock:
            connection = conn
        print(f"Conexión establecida con {addr}")
        sock.close()

    def connect_to_peer():
        nonlocal connection
        for attempt in range(5):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((peer_host, peer_port))
                with lock:
                    connection = sock
                print(f"Conectado exitosamente a {peer_host}:{peer_port}")
                return
            except Exception as e:
                print(f"Intento {attempt+1}/5 fallido: {str(e)}")
                if attempt < 4:
                    time.sleep(2)
        print("No se pudo establecer conexión con el peer")

    if peer_host and peer_port:
        connector = threading.Thread(target=connect_to_peer)
        connector.start()
        connector.join(timeout=15)

    acceptor = threading.Thread(target=accept_connections)
    acceptor.start()

    start_time = time.time()
    while True:
        with lock:
            if connection:
                break
        if time.time() - start_time > 20:
            print("Timeout: No se estableció conexión")
            return
        time.sleep(0.1)

    def sync_loop():
        nonlocal sync_active
        while sync_active and not game.game_over:
            try:
                with lock:
                    current_state = game.get_state()
                    if connection:
                        try:
                            data = json.dumps(current_state).encode('utf-8')
                            msg_len = len(data).to_bytes(4, byteorder='big')
                            connection.sendall(msg_len + data)
                        except (BrokenPipeError, OSError) as e:
                            print(f"Error de conexión: {str(e)}")
                            sync_active = False
                            break

                if connection:
                    try:
                        data = recv_all(connection)
                        if data:
                            peer_state = json.loads(data)
                            with lock:
                                game.set_state(peer_state)
                    except Exception as e:
                        print(f"Error recibiendo datos: {str(e)}")
                        if "10038" in str(e):
                            print("Conexión cerrada por el peer")
                            sync_active = False
                            break

            except Exception as e:
                print(f"Error crítico: {str(e)}")
                sync_active = False
                break

    sync_thread = threading.Thread(target=sync_loop)
    sync_thread.start()

    while True:
        while not game.game_over:
            with lock:
                scenario = game.get_scenario()
            
            print("\n" + "="*50)
            print(scenario["scenario"])
            print("="*50)

            if scenario["choices"] and not scenario_processed:
                while True:
                    try:
                        choice = int(input("\nTu decisión (1/2): "))
                        if choice in [1, 2]:
                            game.player_decision = choice
                            break
                        print("Opción inválida! Solo 1 o 2")
                    except:
                        print("Entrada inválida! Solo números")

                print("\nEsperando decisión del compañero...")
            
                # Nueva condición de espera activa
                start_wait = time.time()
                while True:
                    with lock:
                        if game.other_player_decision is not None:
                            break
                        if time.time() - start_wait > 30:
                            print("\nTiempo de espera agotado!")
                            sync_active = False
                            break
                    time.sleep(0.1)

                if not sync_active:
                    break

                # Procesamiento conjunto sincronizado
                with lock:
                    prev_scenario = game.current_scenario
                    game.process_decisions()
                    
                    # Forzar sincronización del nuevo estado
                    current_state = game.get_state()
                    if connection:
                        data = json.dumps(current_state).encode('utf-8')
                        msg_len = len(data).to_bytes(4, byteorder='big')
                        connection.sendall(msg_len + data)
                    
                    print(f"\nEstado actualizado - Escenario: {game.current_scenario}")
                    
                    # Resetear solo si hay nuevo escenario con opciones
                    if game.current_scenario != prev_scenario and scenario["choices"]:
                        game.reset_decisions()
                        scenario_processed = True

                input("\nPresiona Enter para continuar...")
                scenario_processed = False
            else:
                print("\n" + "="*50)
                print("JUEGO TERMINADO - Resultado final:")
                print(game.game_result)
                break

        restart = input("\n¿Jugar de nuevo? (s/n): ").lower()
        game.reset_game(restart == 's')

        with lock:
            if connection and sync_active:
                try:
                    data = json.dumps(
                        {"restart": game.restart}).encode('utf-8')
                    msg_len = len(data).to_bytes(4, byteorder='big')
                    connection.sendall(msg_len + data)

                    data = recv_all(connection)
                    if data:
                        peer_restart = json.loads(data)
                        if not peer_restart.get("restart", False):
                            print("\nEl compañero ha decidido no jugar de nuevo")
                            sync_active = False
                except:
                    sync_active = False

        if not game.restart or not sync_active:
            break

    sync_active = False
    if connection:
        connection.close()
