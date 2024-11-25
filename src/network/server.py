import socket

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print("Server is listening on", host, port)

    # Espera por una conexión entrante
    client_socket, client_address = server_socket.accept()
    print("Connection established with", client_address)

    try:
        # Enviar mensaje de bienvenida al cliente
        client_socket.sendall("Welcome to the Peer-to-Peer Decision-Making Game!".encode())

        # Esperar respuesta del cliente
        response = client_socket.recv(1024).decode()
        print("Client response:", response)

    except Exception as e:
        print(f"Error during communication: {e}")
    finally:
        # Cerrar la conexión con el cliente
        client_socket.close()
        print("Server connection closed.")

if __name__ == "__main__":
    start_server("localhost", 12345)
