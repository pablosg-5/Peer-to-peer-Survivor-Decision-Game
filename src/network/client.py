import socket

def start_client(server_ip, server_port):
    """ Función para manejar la lógica del cliente. """
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))
        print(f"Successfully connected to {server_ip}:{server_port}")
        
        while True:
            # Recibir el mensaje de bienvenida o el escenario del servidor
            server_message = client_socket.recv(1024).decode()
            if not server_message:
                break
            print(f"Server: {server_message}")
            
            # Si el mensaje contiene el escenario, el cliente puede responder
            if "decision" in server_message.lower():
                client_response = input("Your response: ")
                client_socket.sendall(client_response.encode())
                
                # Recibir el resultado de la elección
                result_message = client_socket.recv(1024).decode()
                print(f"Server response: {result_message}")
                
            # Si el mensaje indica que el juego ha terminado, salir
            if "Game over" in server_message:
                break
    except Exception as e:
        print(f"Failed to connect: {e}")
    finally:
        client_socket.close()
