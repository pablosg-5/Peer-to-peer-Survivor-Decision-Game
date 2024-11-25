import socket

def start_server(host='localhost', port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1) 

    print(f"Server listening on {host}:{port}...")

    connection, client_address = server_socket.accept()  
    print(f"Connected to {client_address}")

    try:
        while True:
            data = connection.recv(1024)
            if data:
                print(f"Received: {data.decode()}")
                connection.sendall(data)  # Echo back the received message
            else:
                break
    finally:
        connection.close()

if __name__ == '__main__':
    start_server()
