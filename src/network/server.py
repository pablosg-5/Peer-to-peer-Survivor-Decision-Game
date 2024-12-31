import socket
from game import Game

def handle_client(client_socket):
    """ Maneja la interacción con el cliente, enviando escenarios y recibiendo respuestas. """
    game = Game()  # Crear una instancia del juego
    player1_choice = None  # Elección del servidor
    player2_choice = None  # Elección del cliente

    try:
        # Enviar la bienvenida y el primer escenario
        client_socket.sendall("Welcome to the game! Here's your first decision:\n".encode())
        
        while True:
            scenario = game.get_scenario()
            if not scenario:
                client_socket.sendall("Game over! Thank you for playing.\n".encode())
                break

            # Enviar escenario a ambos jugadores (servidor y cliente)
            client_socket.sendall(scenario['question'].encode())
            print(scenario['question'])
            
            # Elección del servidor
            player1_choice = input("Your response (Server): ")

            # Esperar la respuesta del cliente
            client2_response = client_socket.recv(1024).decode().strip()

            # Procesar las respuestas y determinar las repercusiones
            result = game.process_choices(player1_choice, client2_response)
            client_socket.sendall(result.encode())

            # Avanzar al siguiente escenario
            game.next_scenario()
            
    except Exception as e:
        print(f"An error occurred with the client: {e}")
    finally:
        # Cerrar la conexión con el cliente
        client_socket.close()
        print("Server connection closed.")

def start_server(host, port):
    """ Inicia el servidor y espera por clientes. """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server is listening on {host}:{port}...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")
        handle_client(client_socket)

if __name__ == "__main__":
    start_server("localhost", 12345)

