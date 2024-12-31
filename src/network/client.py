import socket
import threading

# Función para recibir mensajes del servidor
def receive_messages(client_socket):
    while True:
        message = client_socket.recv(1024).decode()
        if message:
            print(f"Server says: {message}")
        else:
            break

# Función para enviar mensajes al servidor
def send_messages(client_socket):
    while True:
        choice = input("Client: Choose your action (e.g., attack, defend): ")
        client_socket.sendall(choice.encode())  # Enviar la elección al servidor

# Función para iniciar el cliente
def start_client(server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect((server_ip, server_port))
        print(f"Successfully connected to {server_ip}:{server_port}")

        # Crear hilos para recibir y enviar mensajes
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        send_thread = threading.Thread(target=send_messages, args=(client_socket,))
        
        # Iniciar los hilos
        receive_thread.start()
        send_thread.start()

        # Esperar a que los hilos terminen (esto puede ser modificado según la lógica del juego)
        receive_thread.join()
        send_thread.join()

    except Exception as e:
        print(f"Failed to connect: {e}")
    finally:
        client_socket.close()
