import socket
import json
import random
import time
from network.p2p import start_p2p

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except:
        return "127.0.0.1"

def find_available_port(start=5000, end=6000):
    for port in random.sample(range(start, end+1), end-start+1):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(("0.0.0.0", port))
            s.close()
            return port
        except:
            continue
    raise Exception("No ports available")

def connect_to_matchmaking_server(server_ip, server_port, username, local_ip, local_port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((server_ip, server_port))
        sock.sendall(json.dumps({
            "username": username,
            "ip": local_ip,
            "port": local_port
        }).encode())
        
        while True:
            data = sock.recv(1024).decode()
            if not data:
                continue
            response = json.loads(data)
            if response.get("status") == "matched":
                return response
            elif response.get("status") == "waiting":
                print("Waiting for more players...")
                time.sleep(2)
    except Exception as e:
        print(f"Connection error: {e}")
        return None
    finally:
        sock.close()

def main():
    """Main function to start the matchmaking process and establish a P2P connection."""
    print("\n\nWelcome to the True Peer-to-Peer Decision-Making Game!")
    time.sleep(2)
    username = input("\nEnter your username: ")
    local_ip = get_local_ip()
    listen_port = find_available_port()  # Declaración correcta de listen_port

    print(f"Your IP address: {local_ip}")
    print(f"Your port: {listen_port}")
    print("Connecting to matchmaking server...")

    response = connect_to_matchmaking_server(
        "127.0.0.1", 5000, username, local_ip, listen_port)

    if response and response["status"] == "matched":
        print(f"\n✅ Matched with {', '.join([p['username'] for p in response['peers']])}")
        start_p2p(
            host=local_ip,
            port=listen_port,  # Usar la variable declarada
            username=username,
            peers=response["peers"]
        )
    else:
        print("Failed to find a match.")

if __name__ == "__main__":
    main()