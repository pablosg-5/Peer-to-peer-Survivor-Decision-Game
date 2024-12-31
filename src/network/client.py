import socket
from game import Game

def start_client(server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect((server_ip, server_port))
        print(f"Successfully connected to {server_ip}:{server_port}")
        
        # Recibir y mostrar el escenario
        scenario = client_socket.recv(1024).decode()
        print("Server says:", scenario)
        
        # Tomar la decisión
        decision = int(input("Your choice (1 or 2): "))
        client_socket.sendall(str(decision).encode())
        
        # Recibir y mostrar el resultado
        result = client_socket.recv(1024).decode()
        print(result)
        
    except Exception as e:
        print(f"Failed to connect: {e}")
    
    finally:
        client_socket.close()
