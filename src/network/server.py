import socket
import threading
import json

HOST = "0.0.0.0"
PORT = 5000
players_waiting = []
lock = threading.Lock()  # Lock to synchronize access to players_waiting


def handle_client(client_socket, client_address):
    global players_waiting
    try:
        data = client_socket.recv(1024).decode()
        player_info = json.loads(data)
        username = player_info["username"]
        player_port = player_info["port"]
        player_ip = player_info["ip"]

        print(f"Player {username} connected from {player_ip}:{player_port}")

        with lock:
            players_waiting.append(
                (username, player_ip, player_port, client_socket))
            if len(players_waiting) >= 2:
                # Pairing players
                player1 = players_waiting.pop(0)
                player2 = players_waiting.pop(0)

                # Send information to player 1
                try:
                    player1_socket = player1[3]
                    player1_socket.sendall(json.dumps({
                        "status": "matched",
                        "peer_host": player2[1],
                        "peer_port": player2[2],
                        "peer_username": player2[0]
                    }).encode())
                    player1_socket.close()
                except Exception as e:
                    print(f"Error sending data to player 1: {e}")

                # Send information to player 2
                try:
                    player2_socket = player2[3]
                    player2_socket.sendall(json.dumps({
                        "status": "matched",
                        "peer_host": player1[1],
                        "peer_port": player1[2],
                        "peer_username": player1[0]
                    }).encode())
                    player2_socket.close()
                except Exception as e:
                    print(f"Error sending data to player 2: {e}")

    except Exception as e:
        print(f"Error: {e}")
        client_socket.close()  # Close in case of an error


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Matchmaking server started")

    while True:
        client_socket, client_address = server.accept()
        client_thread = threading.Thread(
            target=handle_client, args=(client_socket, client_address))
        client_thread.start()


if __name__ == "__main__":
    start_server()
