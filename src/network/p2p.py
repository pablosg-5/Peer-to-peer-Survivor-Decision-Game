import socket
import json
import threading
import time
from game import Game

def recv_all(sock):
    """Recibe datos con prefijo de longitud de forma confiable"""
    try:
        raw_len = sock.recv(4)
        if not raw_len:
            return None
        msg_len = int.from_bytes(raw_len, byteorder='big')
        data = b""
        while len(data) < msg_len:
            packet = sock.recv(min(4096, msg_len - len(data)))
            if not packet:
                return None
            data += packet
        return data.decode()
    except:
        return None

def send_data(sock, data):
    """Envía datos con prefijo de longitud"""
    try:
        msg = json.dumps(data).encode()
        sock.sendall(len(msg).to_bytes(4, 'big') + msg)
    except:
        pass

def start_p2p(host, port, peer_host=None, peer_port=None):
    game = Game()
    connection = None
    lock = threading.Lock()
    sync_active = True

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
        for _ in range(5):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((peer_host, peer_port))
                with lock:
                    connection = sock
                print(f"Conectado exitosamente a {peer_host}:{peer_port}")
                return
            except:
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
            with lock:
                if connection:
                    send_data(connection, game.get_state())
                    data = recv_all(connection)
                    if data:
                        game.set_state(json.loads(data))
            time.sleep(0.1)

    sync_thread = threading.Thread(target=sync_loop)
    sync_thread.start()

    while True:
        while not game.game_over:
            scenario = game.get_scenario()
            print("\n" + "=" * 50)
            print(scenario["scenario"])
            print("=" * 50)
            
            if scenario["choices"]:
                choice = None
                while choice not in [1, 2]:
                    try:
                        choice = int(input("\nTu decisión (1/2): "))
                    except:
                        pass
                
                with lock:
                    game.player_decision = choice
                    send_data(connection, {"decision": choice})
                
                print("\nEsperando decisión del compañero...")
                while game.other_player_decision is None and sync_active:
                    data = recv_all(connection)
                    if data:
                        peer_data = json.loads(data)
                        with lock:
                            game.other_player_decision = peer_data.get("decision")
                    time.sleep(0.1)

                if not sync_active:
                    break
                
                print("\n" + "=" * 50)
                print(f"Tu elección: {game.player_decision}")
                print(f"Decisión del compañero: {game.other_player_decision}")
                game.process_decisions()
                game.reset_decisions()
                input("\nPresiona Enter para continuar...")
            else:
                print("\nJUEGO TERMINADO - Resultado final:")
                print(game.game_result)
                break
        
        restart = input("\n¿Jugar de nuevo? (s/n): ").lower() == 's'
        game.reset_game(restart)
        if not restart:
            break
    
    sync_active = False
    if connection:
        connection.close()
