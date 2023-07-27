import socket
import sys

def start_client(server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    print(f"Connected to server: {server_ip}:{server_port}")

    while True:
        message = input("Enter a message ('terminate' to quit): ")
        client_socket.send(message.encode())
        if message == "terminate":
            break

    client_socket.close()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: my_client_app.py <server_ip> <server_port>")
        sys.exit(1)
    
    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    start_client(server_ip, server_port)
