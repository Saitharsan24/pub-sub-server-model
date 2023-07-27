import sys
import socket
import threading

clients = []
publishers = []

def handle_client(client_socket, client_address):
    clients.append(client_socket)
    print(f"New connection from {client_address}")

    while True:
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            break
        print(f"Received from {client_address}: {data}")

        if client_socket in publishers:
            relay_message_to_subscribers(data)

    print(f"Client {client_address} disconnected.")
    clients.remove(client_socket)
    client_socket.close()

def relay_message_to_subscribers(message):
    for client_socket in clients:
        if client_socket in publishers:
            continue
        try:
            client_socket.sendall(message.encode('utf-8'))
        except:
            clients.remove(client_socket)

def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    print(f"Server listening on port {port}")

    while True:
        client_socket, client_address = server_socket.accept()
        client_type = client_socket.recv(1024).decode('utf-8').upper()
        if client_type == 'PUBLISHER':
            publishers.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python my_server_app.py <PORT>")
        sys.exit(1)

    try:
        port = int(sys.argv[1])
    except ValueError:
        print("Invalid PORT. Please provide a valid integer.")
        sys.exit(1)

    start_server(port)
