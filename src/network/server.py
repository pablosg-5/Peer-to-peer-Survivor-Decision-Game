import socket
import threading
import json

HOST = "0.0.0.0"
PORT = 5000
players_waiting = []
lock = threading.Lock()

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
            players_waiting.append((username, player_ip, player_port, client_socket))
            if len(players_waiting) >= 3:
                # Formar grupo de 3 jugadores
                player1 = players_waiting.pop(0)
                player2 = players_waiting.pop(0)
                player3 = players_waiting.pop(0)

                # Función para enviar peers
                def send_peers(target_player, peer1, peer2):
                    try:
                        target_socket = target_player[3]
                        target_socket.sendall(json.dumps({
                            "status": "matched",
                            "peers": [
                                {"username": peer1[0], "ip": peer1[1], "port": peer1[2]},
                                {"username": peer2[0], "ip": peer2[1], "port": peer2[2]}
                            ]
                        }).encode())
                        target_socket.close()
                    except Exception as e:
                        print(f"Error sending data: {e}")

                # Enviar a cada jugador sus 2 peers
                send_peers(player1, player2, player3)
                send_peers(player2, player1, player3)
                send_peers(player3, player1, player2)

    except Exception as e:
        print(f"Error: {e}")
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print("🕹️ Matchmaking server for 3 players started!")

    while True:
        client_socket, client_address = server.accept()
        client_thread = threading.Thread(
            target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == "__main__":
    start_server()