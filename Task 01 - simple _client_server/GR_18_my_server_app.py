import socket
import sys

def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('192.168.56.1', port))
    server_socket.listen(1)
    print(f"Server listening on port {port}")

    client_socket, client_address = server_socket.accept()
    print(f"Connected to client: {client_address}")

    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        print(f"Received from client: {data.decode()}")

    client_socket.close()
    server_socket.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: my_server_app.py <port>")
        sys.exit(1)
    
    port = int(sys.argv[1])
    start_server(port)
