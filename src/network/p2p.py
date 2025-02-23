import socket
import json
import threading
import time
from game import Game

def recv_all(sock):
    """Recibe datos con prefijo de longitud de forma confiable"""
    try:
        # Recibir los 4 bytes del largo del mensaje
        raw_len = b""
        while len(raw_len) < 4:
            chunk = sock.recv(4 - len(raw_len))
            if not chunk:
                return None
            raw_len += chunk
        
        msg_len = int.from_bytes(raw_len, byteorder='big')
        
        # Recibir el mensaje completo
        data = b""
        while len(data) < msg_len:
            packet = sock.recv(min(4096, msg_len - len(data)))
            if not packet:
                return None
            data += packet
        
        return data.decode()
    except ConnectionResetError:
        return None

def start_p2p(host, port, peer_host=None, peer_port=None):
    game = Game()
    connection = None
    lock = threading.Lock()
    last_sent_state = None
    sync_active = True
    last_sent_time = 0  # Nueva variable para control de envíos

    # Hilo para aceptar conexiones (modificado para reintentos)
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

    # Hilo para conectar a peer (con reintentos)
    def connect_to_peer():
        nonlocal connection
        max_retries = 5
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((peer_host, peer_port))
                with lock:
                    connection = sock
                print(f"Conectado exitosamente a {peer_host}:{peer_port}")
                return
            except Exception as e:
                print(f"Intento {attempt+1}/{max_retries} fallido: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
        
        print("No se pudo establecer conexión con el peer")

    # Iniciar conexiones con prioridad
    if peer_host and peer_port:  # Si somos el cliente, conectamos primero
        connector = threading.Thread(target=connect_to_peer)
        connector.start()
        connector.join(timeout=10)
    
    acceptor = threading.Thread(target=accept_connections)
    acceptor.start()

    # Esperar conexión con timeout
    start_time = time.time()
    while True:
        with lock:
            if connection:
                break
        if time.time() - start_time > 15:
            print("Timeout: No se estableció conexión")
            return
        time.sleep(0.1)

    # Bucle de sincronización mejorado
    def sync_loop():
        nonlocal last_sent_state, sync_active, last_sent_time
        while sync_active and not game.game_over:
            try:
                with lock:
                    current_state = game.get_state()
                    # Enviar cada segundo o cuando cambia el estado
                    if connection and (current_state != last_sent_state or (time.time() - last_sent_time) > 1):
                        try:
                            data = json.dumps(current_state).encode()
                            msg_len = len(data).to_bytes(4, byteorder='big')
                            connection.sendall(msg_len + data)
                            last_sent_state = current_state
                            last_sent_time = time.time()
                            print(f"[DEBUG] Enviado estado: {current_state}")
                        except (BrokenPipeError, OSError) as e:
                            print(f"Error de envío: {str(e)}")
                            sync_active = False
                            break
                
                # Recepción optimizada
                with lock:
                    if connection:
                        try:
                            connection.settimeout(0.2)  # Timeout más corto
                            data = recv_all(connection)
                            if data:
                                peer_state = json.loads(data)
                                if peer_state != game.get_state():
                                    print(f"[NET] Estado recibido: Escenario {peer_state['current_scenario']}")  # Mensaje simplificado
                                    game.set_state(peer_state)
                        except socket.timeout:
                            continue
                        except json.JSONDecodeError:
                            print("Error: Mensaje corrupto")
                        except Exception as e:
                            print(f"Error de recepción: {str(e)}")
                            sync_active = False
                            break
            
            except Exception as e:
                print(f"Error crítico: {str(e)}")
                sync_active = False
                break

    sync_thread = threading.Thread(target=sync_loop)
    sync_thread.start()

    # Bucle principal del juego con sincronización forzada inicial
    last_sent_state = None
    while not game.game_over:
        with lock:
            scenario = game.get_scenario()
        
        print("\033c", end="")
        print("="*50)
        print(scenario["scenario"] + "\n")
        
        if scenario["choices"]:
            with lock:
                status = []
                if game.player_decision is not None:
                    status.append(f"Tu elección: {game.player_decision}")
                if game.other_player_decision is not None:
                    status.append(f"Compañero: {game.other_player_decision}")
                
                if status:
                    print("Estado actual:", " | ".join(status))
            
            # Input optimizado
            with lock:
                if game.player_decision is None:
                    try:
                        choice = int(input("\nTu decisión (1/2): "))
                        if choice not in scenario["choices"]:
                            print("Opción inválida!")
                            continue
                        game.player_decision = choice
                        last_sent_state = None
                    except:
                        print("Entrada debe ser 1 o 2")
                        continue
            
            # Espera activa optimizada
            wait_start = time.time()
            while not game.game_over:
                with lock:
                    current_state = game.get_state()
                    if current_state["other_player_decision"] is not None:
                        print("\n¡Decisión recibida!")
                        break
                
                if time.time() - wait_start > 10:
                    print("\n¡Tiempo agotado! (10s)")
                    with lock:
                        sync_active = False
                        game.game_over = True
                    break
                
                print(f"Esperando... [{int(time.time()-wait_start)}s]", end="\r")
                time.sleep(0.1)
            # Procesamiento final
            with lock:
                if game.player_decision is not None and game.other_player_decision is not None:
                    game.process_decisions()
                    print("\n" + "="*50)
                    print(f"Progresando al escenario {game.current_scenario}")
                    game.reset_decisions()
                    input("Presiona Enter para continuar...")
                    last_sent_state = None
        else:
            print("\n" + "="*50)
            print("JUEGO TERMINADO")
            print(game.game_result)
            break

    sync_active = False
    if connection:
        connection.close()