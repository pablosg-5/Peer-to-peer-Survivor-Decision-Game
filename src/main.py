import socket
import json
import random
import time
from network.p2p import start_p2p

# ==============================================
# Network Utilities
# ==============================================


def get_local_ip():
    """
    Get the machine's local IP address using a UDP socket hack.
    Falls back to 127.0.0.1 if connection fails.
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Connect to Google's DNS server
        return s.getsockname()[0]
    except:
        return "127.0.0.1"


def find_available_port(start=5000, end=6000):
    """
    Find a random available port in specified range.
    Uses random sampling to reduce port collision chances.
    """
    for port in random.sample(range(start, end+1), end-start+1):
        try:
            # Test port availability with temporary socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(("0.0.0.0", port))
            s.close()
            return port
        except:
            continue
    raise Exception("No ports available in range {}-{}".format(start, end))

# ==============================================
# Matchmaking Client
# ==============================================


def connect_to_matchmaking_server(server_ip, server_port, username, local_ip, local_port):
    """
    Connect to central matchmaking server and handle matchmaking process.
    Returns:
        - Peer list if matched
        - None on failure
    Handles server communication protocol:
        1. Send player info (username + connection details)
        2. Wait for match confirmation
        3. Return peer list when match is ready
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((server_ip, server_port))

        # Send player registration data
        registration_data = {
            "username": username,
            "ip": local_ip,
            "port": local_port
        }
        sock.sendall(json.dumps(registration_data).encode())

        # Server communication loop
        while True:
            data = sock.recv(1024).decode()
            if not data:
                continue  # Keep alive

            response = json.loads(data)

            # Handle different server responses
            if response.get("status") == "matched":
                print("Match found!")
                return response
            elif response.get("status") == "waiting":
                print("Waiting for more players...")
                time.sleep(2)  # Prevent busy waiting

    except Exception as e:
        print(f"Matchmaking error: {e}")
        return None
    finally:
        sock.close()

# ==============================================
# Main Game Launcher
# ==============================================


def main():
    print("\n\nWelcome to the True Peer-to-Peer Decision-Making Game!")
    time.sleep(1)  # Pause for better readability

    # User setup
    username = input("\nEnter your username: ").strip()
    local_ip = get_local_ip()
    listen_port = find_available_port()  # Dynamic port allocation

    # Network info display
    print(f"\n🌐 Your connection details:")
    print(f"IP Address: {local_ip}")
    print(f"Port: {listen_port}")
    print("Connecting to matchmaking server...")

    # Matchmaking phase
    response = connect_to_matchmaking_server(
        server_ip="127.0.0.1",
        server_port=5000,
        username=username,
        local_ip=local_ip,
        local_port=listen_port
    )

    # Game launch logic
    if response and response["status"] == "matched":
        print(f"\n✅ Match successful! Players:",
              ", ".join([p['username'] for p in response['peers']]))

        # Start P2P game engine
        start_p2p(
            host=local_ip,
            port=listen_port,
            username=username,
            peers=response["peers"]
        )
    else:
        print("\n❌ Failed to find a match. Please try again later.")


if __name__ == "__main__":
    main()
