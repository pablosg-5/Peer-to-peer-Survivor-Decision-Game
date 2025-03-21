import socket
import json
import random
import time
from network.p2p import start_p2p


def get_local_ip():
    """Gets the local IP address of the machine."""
    try:
        # Connect to an external server to determine the local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Google DNS
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        print(f"Error getting local IP: {e}")
        return "127.0.0.1"  # Fallback to localhost


def find_available_port(start_port=5000, end_port=6000):
    """Finds an available port within the specified range."""
    ports = list(range(start_port, end_port + 1))
    random.shuffle(ports)  # Avoid conflicts between clients

    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                s.bind(("0.0.0.0", port))
                return port
            except OSError:
                continue
    raise Exception("No available ports")


def connect_to_matchmaking_server(host, port, username, local_ip, listen_port):
    """Connects to the matchmaking server and returns the response."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))

        # Send data once
        sock.sendall(json.dumps({
            "username": username,
            "ip": local_ip,
            "port": listen_port
        }).encode())

        # Actively wait for a response
        while True:
            response = sock.recv(1024).decode()
            if not response:
                time.sleep(1)
                continue

            data = json.loads(response)
            if data.get("status") == "matched":
                return data
            elif data.get("status") == "waiting":
                print("Waiting for another player...")
                time.sleep(2)

    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        sock.close()  # Close only at the end


def main():
    """Main function to start the matchmaking process and establish a P2P connection."""
    print("\n\nWelcome to the True Peer-to-Peer Decision-Making Game!")
    time.sleep(2)
    username = input("\nEnter your username: ")
    local_ip = get_local_ip()
    listen_port = find_available_port()

    print(f"Your IP address: {local_ip}")
    print(f"Your port: {listen_port}")
    print("Connecting to matchmaking server...")

    response = connect_to_matchmaking_server(
        "127.0.0.1", 5000, username, local_ip, listen_port)

    if response and response["status"] == "matched":
        peer_host = response["peer_host"]
        peer_port = response["peer_port"]
        peer_username = response["peer_username"]
        time.sleep(2)
        print(f"\n✅ Matched with {peer_username}")

        # Start P2P symmetrically
        start_p2p(
            host=local_ip,
            port=listen_port,
            peer_host=peer_host,
            peer_port=peer_port,
            peer_username=peer_username
        )
    else:
        print("Failed to find a match.")


if __name__ == "__main__":
    main()
