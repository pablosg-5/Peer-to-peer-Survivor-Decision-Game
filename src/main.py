import sys
from network.server import start_server
from network.client import start_client

def main():
    print("Welcome to the Peer-to-Peer Decision-Making Game!")
    
    # Preguntar al jugador si desea ser el servidor o el cliente
    choice = input("Do you want to host the game as a server (s) or connect as a client (c)? ").lower()

    if choice == 's':
        print("You are now the server!")
        host = input("Enter the host IP address (or press Enter for localhost): ") or "127.0.0.1"  # Default to localhost if no input
        port = int(input("Enter the port number: "))  
        start_server(host, port)  # Llama a la función del servidor
    elif choice == 'c':
        server_ip = input("Enter the server IP address: ")
        server_port = int(input("Enter the server port: "))  
        print(f"Connecting to {server_ip}:{server_port}...")
        start_client(server_ip, server_port)  # Llama a la función del cliente
    else:
        print("Invalid choice! Exiting.")
        sys.exit(1)

if __name__ == "__main__":
    main()
