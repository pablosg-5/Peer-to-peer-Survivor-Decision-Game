import sys
from network.p2p import start_p2p


def main():
    print("Welcome to the Peer-to-Peer Decision-Making Game!")

    # Preguntar si el usuario quiere ser servidor o cliente
    choice = input(
        "Do you want to host the game as a server (s) or connect as a client (c)? ").lower()

    if choice == 's':
        print("You are now the server! Waiting for a connection...")
        host = input(
            "Enter the host IP address (or press Enter for localhost): ") or "127.0.0.1"
        port = int(input("Enter the port number: "))
        start_p2p(host, port, is_server=True)
    elif choice == 'c':
        print("You are now the client! Connecting to the server...")
        server_ip = input("Enter the server IP address: ")
        server_port = int(input("Enter the server port: "))
        start_p2p(server_ip, server_port, is_server=False)
    else:
        print("Invalid choice! Exiting.")
        sys.exit(1)


if __name__ == "__main__":
    main()
