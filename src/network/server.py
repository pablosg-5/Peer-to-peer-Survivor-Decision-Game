# ==============================================
# Matchmaking Server
# ==============================================

import socket
import threading
import json

# Server configuration
HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 5000        # Default matchmaking port
players_waiting = []  # Player queue
lock = threading.Lock()  # Thread safety for shared resources


def handle_client(client_socket, client_address):
    """
    Handle client connections for matchmaking:
    1. Receive player registration data
    2. Add to waiting queue
    3. Form 3-player groups when possible
    4. Distribute peer connection info
    """
    global players_waiting
    try:
        # Receive and parse player data
        data = client_socket.recv(1024).decode()
        player_info = json.loads(data)
        username = player_info["username"]
        player_port = player_info["port"]
        player_ip = player_info["ip"]

        print(f"Player {username} connected from {player_ip}:{player_port}\n")

        with lock:  # Thread-safe queue modification
            players_waiting.append(
                (username, player_ip, player_port, client_socket))

            # Form group when 3 players available
            if len(players_waiting) >= 3:
                player1 = players_waiting.pop(0)
                player2 = players_waiting.pop(0)
                player3 = players_waiting.pop(0)

                def send_peers(target_player, peer1, peer2):
                    # Send peer information to a player and close connection
                    try:
                        target_socket = target_player[3]
                        target_socket.sendall(json.dumps({
                            "status": "matched",
                            "peers": [
                                {"username": peer1[0],
                                    "ip": peer1[1], "port": peer1[2]},
                                {"username": peer2[0],
                                    "ip": peer2[1], "port": peer2[2]}
                            ]
                        }).encode())
                        target_socket.close()
                    except Exception as e:
                        print(f"Error sending data: {e}")

                # Distribute peer info to all group members
                send_peers(player1, player2, player3)
                send_peers(player2, player1, player3)
                send_peers(player3, player1, player2)

    except Exception as e:
        print(f"Connection error: {e}")
        client_socket.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print("🕹️  Matchmaking server for 3 players started!\n")

    while True:
        client_socket, client_address = server.accept()
        client_thread = threading.Thread(
            target=handle_client, args=(client_socket, client_address))
        client_thread.start()


if __name__ == "__main__":
    start_server()
