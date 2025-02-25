import socket
import json
import threading
import time
from game import Game


def recv_data(sock):
    """Recibe un mensaje JSON del socket."""
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
    """Envía un mensaje JSON a través del socket."""
    try:
        data = json.dumps(message).encode('utf-8')
        msg_len = len(data).to_bytes(4, byteorder='big')
        sock.sendall(msg_len + data)
    except (BrokenPipeError, OSError):
        pass


def handle_peer_connection(sock, game):
    """Maneja la recepción de decisiones del otro jugador."""
    while not game.game_over:
        peer_decision = recv_data(sock)
        if peer_decision and "decision" in peer_decision:
            game.other_player_decision = peer_decision["decision"]
        time.sleep(0.1)


def start_p2p(host, port, peer_host=None, peer_port=None):
    game = Game()
    connection = None
    lock = threading.Lock()

    def accept_connection():
        """Espera una conexión entrante."""
        nonlocal connection
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen(1)
        print(f"Esperando conexión en {host}:{port}...")
        conn, addr = server.accept()
        with lock:
            connection = conn
        print(f"Conectado con {addr}")
        server.close()

    def connect_to_peer():
        """Intenta conectar con el otro jugador."""
        nonlocal connection
        time.sleep(1)  # Pequeña pausa para evitar colisiones
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((peer_host, peer_port))
            with lock:
                connection = sock
            print(f"Conectado con {peer_host}:{peer_port}")
        except Exception as e:
            print(f"Error conectando al peer: {str(e)}")

    if peer_host and peer_port:
        threading.Thread(target=connect_to_peer, daemon=True).start()

    accept_thread = threading.Thread(target=accept_connection, daemon=True)
    accept_thread.start()
    accept_thread.join(timeout=10)

    if not connection:
        print("No se pudo establecer la conexión.")
        return

    # Hilo para manejar la comunicación entrante
    threading.Thread(target=handle_peer_connection, args=(
        connection, game), daemon=True).start()

    while not game.game_over:
        scenario = game.get_scenario()
        print("\n" + "="*50)
        print(scenario["scenario"])
        print("="*50)

        if scenario["choices"]:
            while True:
                try:
                    choice = int(input("\nTu decisión (1/2): "))
                    if choice in [1, 2]:
                        with lock:
                            game.player_decision = choice
                        send_data(connection, {"decision": choice})
                        break
                    print("Opción inválida! Solo 1 o 2")
                except ValueError:
                    print("Entrada inválida! Solo números")

            print("\nEsperando decisión del compañero...")
            while game.other_player_decision is None:
                time.sleep(0.1)

            game.process_decisions()
            game.other_player_decision = None  # Reset para la siguiente ronda
            input("\nPresiona Enter para continuar...")
        else:
            print("\nJuego terminado.")
            break

    connection.close()
