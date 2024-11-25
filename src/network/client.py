import socket

def start_client(server_ip='localhost', server_port=12345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port)) 

    try:
        message = "Hello from client!"
        print(f"Sending: {message}")
        client_socket.sendall(message.encode())

        data = client_socket.recv(1024)
        print(f"Received: {data.decode()}")
    finally:
        client_socket.close()

if __name__ == '__main__':
    start_client()
