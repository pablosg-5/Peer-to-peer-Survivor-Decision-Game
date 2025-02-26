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
        print(f"🔌 Servidor escuchando en {self.host}:{self.port}")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"🟢 Nueva conexión entrante de {addr}")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024).decode()
                if not data:
                    break
                print(f"\n📩 Mensaje recibido: {data}")
            except:
                break
        client_socket.close()

    def connect_to_peer(self, peer_host, peer_port):
        try:
            peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peer_socket.connect((peer_host, peer_port))
            self.peers.append(peer_socket)
            print(f"✅ Conectado a {peer_host}:{peer_port}")
            return peer_socket
        except Exception as e:
            print(f"❌ Error conectando a {peer_host}:{peer_port}: {e}")
            return None

    def send_message(self, peer_socket, message):
        try:
            peer_socket.send(message.encode())
            print(f"📤 Mensaje enviado: {message}")
        except Exception as e:
            print(f"Error enviando mensaje: {e}")

def start_node(port):
    node = P2PNode('127.0.0.1', port)
    server_thread = threading.Thread(target=node.start_server)
    server_thread.daemon = True
    server_thread.start()

    time.sleep(1)  # Esperar que el servidor inicie

    while True:
        try:
            peer_port = int(input("\nIngrese puerto del peer a conectar (0 para saltar): "))
            if peer_port == 0:
                break
            peer_socket = node.connect_to_peer('127.0.0.1', peer_port)
            if peer_socket:
                message = input("Escribe un mensaje (o 'exit' para salir): ")
                while message.lower() != 'exit':
                    node.send_message(peer_socket, message)
                    message = input("Escribe un mensaje (o 'exit' para salir): ")
        except ValueError:
            print("⚠️ Puerto inválido")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Uso: python p2p_test.py <puerto>")
        sys.exit(1)
    
    start_node(int(sys.argv[1]))