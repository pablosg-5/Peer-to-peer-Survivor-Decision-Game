import sys
from network.server import start_server_connection
from network.client import start_client

def main():
    print("Welcome to the Peer-to-Peer Decision-Making Game!")
    
    choice = input("Do you want to host the game as a server (s) or connect as a client (c)? ").lower()

    if choice == 's':
        print("You are now the server!")
        host = input("Enter the host IP address (or press Enter for localhost): ") or "127.0.0.1"  # Default to localhost
        port = int(input("Enter the port number: "))
        start_server_connection(host, port)
    elif choice == 'c':
        server_ip = input("Enter the server IP address: ")
        server_port = int(input("Enter the server port: "))
        print(f"Connecting to {server_ip}:{server_port}...")
        start_client(server_ip, server_port)
    else:
        print("Invalid choice! Exiting.")
        sys.exit(1)

if __name__ == "__main__":
    main()
