import socket
from game import Game
import threading

def handle_client(client_socket, game):
    try:
        while game.current_scenario < len(game.scenarios):
            # Enviar escenario al cliente
            scenario = game.get_scenario(game.current_scenario)
            client_socket.sendall(scenario["scenario"].encode())

            # Recibir la decisión del cliente
            other_decision = client_socket.recv(1024).decode()
            game.other_player_decision = other_decision

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

def start_p2p(host, port, is_server):
    game = Game()  # Instancia compartida (solo para lógica local)

    if is_server:
        # Configurar servidor
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"Server en {host}:{port}...")

        # Aceptar conexión
        client_socket, addr = server_socket.accept()
        print(f"Conectado a {addr}")

        # Hilo para manejar al cliente
        threading.Thread(target=handle_client, args=(client_socket, game)).start()

        # Lógica del servidor
        while game.current_scenario < len(game.scenarios):
            scenario = game.get_scenario(game.current_scenario)
            print(f"\nEscenario {game.current_scenario + 1}: {scenario['scenario']}")

            # Obtener decisión del servidor
            decision = input("Tu decisión (1/2): ")
            client_socket.sendall(decision.encode())  # Enviar decisión al cliente

            # Esperar respuesta del cliente
            while game.other_player_decision is None:
                pass  # Espera activa hasta recibir decisión

            # Mostrar resultados
            print(f"\nTu elección: {decision}")
            print(f"Elección del otro jugador: {game.other_player_decision}")
            game.current_scenario += 1
            game.other_player_decision = None  # Resetear para el siguiente escenario

        server_socket.close()

    else:
        # Configurar cliente
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        print(f"Conectado a {host}:{port}")

        # Lógica del cliente
        while game.current_scenario < len(game.scenarios):
            # Recibir escenario del servidor
            scenario = client_socket.recv(1024).decode()
            print(f"\nEscenario {game.current_scenario + 1}: {scenario}")

            # Obtener decisión del cliente
            decision = input("Tu decisión (1/2): ")
            client_socket.sendall(decision.encode())  # Enviar decisión al servidor

            # Esperar respuesta del servidor
            other_decision = client_socket.recv(1024).decode()
            print(f"\nTu elección: {decision}")
            print(f"Elección del otro jugador: {other_decision}")
            game.current_scenario += 1

        client_socket.close()