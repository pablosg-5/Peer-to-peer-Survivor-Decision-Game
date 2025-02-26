import socket
import threading
import time

class P2PNode:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.peers = []

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"🔌 Server listening on {self.host}:{self.port}")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"🟢 New incoming connection from {addr}")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024).decode()
                if not data:
                    break
                print(f"\n📩 Message received: {data}")
            except:
                break
        client_socket.close()

    def connect_to_peer(self, peer_host, peer_port):
        try:
            peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peer_socket.connect((peer_host, peer_port))
            self.peers.append(peer_socket)
            print(f"✅ Connected to {peer_host}:{peer_port}")
            return peer_socket
        except Exception as e:
            print(f"❌ Error connecting to {peer_host}:{peer_port}: {e}")
            return None

    def send_message(self, peer_socket, message):
        try:
            peer_socket.send(message.encode())
            print(f"📤 Message sent: {message}")
        except Exception as e:
            print(f"Error sending message: {e}")

def start_node(port):
    node = P2PNode('127.0.0.1', port)
    server_thread = threading.Thread(target=node.start_server)
    server_thread.daemon = True
    server_thread.start()

    time.sleep(1)  # Wait for the server to start

    while True:
        try:
            peer_port = int(input("\nEnter the peer's port to connect to (0 to skip): "))
            if peer_port == 0:
                break
            peer_socket = node.connect_to_peer('127.0.0.1', peer_port)
            if peer_socket:
                message = input("Type a message (or 'exit' to quit): ")
                while message.lower() != 'exit':
                    node.send_message(peer_socket, message)
                    message = input("Type a message (or 'exit' to quit): ")
        except ValueError:
            print("⚠️ Invalid port")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python p2p_test.py <port>")
        sys.exit(1)
    
    start_node(int(sys.argv[1]))
