import socket
import threading

# Función para manejar la comunicación con el cliente
def handle_client(client_socket):
    try:
        # Enviar mensaje de bienvenida al cliente
        client_socket.sendall("Welcome to the Peer-to-Peer Decision-Making Game!".encode())

        # Recibir la primera respuesta del cliente
        response = client_socket.recv(1024).decode()
        print("Client response:", response)

        # Aquí es donde se agregan las situaciones de elección del juego
        while True:
            choice = input("Server: Choose your action (e.g., attack, defend): ")
            client_socket.sendall(choice.encode())  # Enviar al cliente

            # Esperar respuesta del cliente
            client_response = client_socket.recv(1024).decode()
            print(f"Client chose: {client_response}")

            # Lógica del juego basada en las elecciones del servidor y el cliente
            if choice == client_response:
                print("Both chose the same action. You both survive!")
            else:
                print("Different choices. Consequences will occur!")
            break  # Terminar después de una ronda

    except Exception as e:
        print(f"Error during communication: {e}")
    finally:
        client_socket.close()
        print("Server connection closed.")

# Función para iniciar el servidor
def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print("Server is listening on", host, port)

    # Esperar por una conexión entrante
    client_socket, client_address = server_socket.accept()
    print("Connection established with", client_address)

    # Crear un hilo para manejar la comunicación con el cliente
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()

if __name__ == "__main__":
    start_server("localhost", 12345)
