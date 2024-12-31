import socket
from game import Game

def handle_client(client_socket, game):
    try:
        # Enviar escenario al cliente
        scenario = game.get_scenario(0)  # Usamos el primer escenario
        client_socket.sendall(scenario["scenario"].encode())

        # Recibir la decisión del cliente
        decision = int(client_socket.recv(1024).decode())
        game.process_decision(decision)

        # Enviar los resultados al cliente
        results = game.get_results()
        client_socket.sendall(f"Results: {', '.join(results)}".encode())
        
    except Exception as e:
        print(f"Error during game communication: {e}")
    finally:
        client_socket.close()

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print("Server is listening on", host, port)

    # Esperar por una conexión entrante
    client_socket, client_address = server_socket.accept()
    print("Connection established with", client_address)

    game = Game()  # Crear una instancia del juego
    handle_client(client_socket, game)
    print("Server connection closed.")
