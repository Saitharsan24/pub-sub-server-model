import sys
import socket

def start_client(server_ip, port, client_type):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((server_ip, port))
    except ConnectionRefusedError:
        print(f"Connection to server at {server_ip}:{port} refused.")
        sys.exit(1)

    client_socket.sendall(client_type.encode('utf-8'))

    if client_type == 'PUBLISHER':
        while True:
            message = input("Enter a message to send to the server (type 'terminate' to exit): ")
            client_socket.sendall(message.encode('utf-8'))
            if message == 'terminate':
                break
    else:  # Subscriber
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            print(f"Received from server: {data}")

    print("Client terminated.")
    client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python my_client_app.py <SERVER_IP> <PORT> <CLIENT_TYPE>")
        print("CLIENT_TYPE should be either 'PUBLISHER' or 'SUBSCRIBER'.")
        sys.exit(1)

    server_ip = sys.argv[1]
    try:
        port = int(sys.argv[2])
    except ValueError:
        print("Invalid PORT. Please provide a valid integer.")
        sys.exit(1)

    client_type = sys.argv[3].upper()
    if client_type not in ('PUBLISHER', 'SUBSCRIBER'):
        print("Invalid CLIENT_TYPE. Should be either 'PUBLISHER' or 'SUBSCRIBER'.")
        sys.exit(1)

    start_client(server_ip, port, client_type)
