import socket
from p2p import start_server

def start_server_connection(host, port):
    start_server(host, port)

if __name__ == "__main__":
    host = input("Enter the host IP address (or press Enter for localhost): ") or "127.0.0.1"  # Default to localhost
    port = int(input("Enter the port number: "))
    start_server_connection(host, port)
