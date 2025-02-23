import sys
from network.p2p import start_p2p

def main():
    print("Welcome to the True Peer-to-Peer Decision-Making Game!")
    
    # Configuración local
    host = input("Enter YOUR IP address (or press Enter for localhost): ") or "127.0.0.1"
    port = int(input("Enter YOUR port number: "))
    
    # Configuración del peer remoto
    peer_host = input("Enter PEER IP address (leave empty if none): ") or None
    peer_port = int(input("Enter PEER port number (0 if none): ") or 0)
    
    start_p2p(
        host=host, 
        port=port,
        peer_host=peer_host if peer_host else None,
        peer_port=peer_port if peer_port else None
    )

if __name__ == "__main__":
    main()