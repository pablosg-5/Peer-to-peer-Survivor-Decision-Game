import socket

def start_client(server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        
        client_socket.connect((server_ip, server_port))
        print(f"Successfully connected to {server_ip}:{server_port}")
        
       
        message = client_socket.recv(1024).decode()
        print("Server says:", message)
        
    except Exception as e:
        print(f"Failed to connect: {e}")
    
    finally:
        client_socket.close()

