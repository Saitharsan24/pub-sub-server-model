import socket
import threading

PORT = 9999
HOST = socket.gethostbyname(socket.gethostname())
ADDR = (HOST, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = 'terminate'

print({HOST})


clients = {}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def display_active_connections_count():
    print(f"[ACTIVE CONNECTIONS]: {len(clients)}")

def start():
    server.listen() # listen for new connections
    print(f'[LISTENING] Server is listening on {HOST}')
    
    while True:
        conn, addr = server.accept()
        client_info = conn.recv(1024).decode(FORMAT).upper().split()
        client_type, topic_name = client_info
        
        # Add the new client to the dictionary with their type and topic
        clients[conn] = (client_type, topic_name)

        print(f"New connection from {addr[0]}:{addr[1]} as {client_type} on topic {topic_name}")
        display_active_connections_count()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


def handle_client(conn,addr):
        
    while True:
        try:
            msg = conn.recv(1024).decode(FORMAT)
            
            if msg == DISCONNECT_MESSAGE:
                break

            # Check if client is registered as a Publisher or Subscriber
            client_type, topic = clients[conn]
            print(f'[{addr}]: {msg}')
            

            if client_type == "PUBLISHER":
                # Forward message to all Subscriber clients interested in the same topic
                for client, (type, tpc) in clients.items():
                    if type == "SUBSCRIBER" and tpc == topic:
                        client.send(msg.encode('utf-8'))
            
            elif client_type == "SUBSCRIBER":
                # Print message to the Subscriber's terminal
                print(msg.decode())            
            
        except Exception as e:
            print(f"Error: {e}")
            break

    # Remove client from the dictionary when they disconnect
    del clients[conn]
    conn.close()
    display_active_connections_count()
    
    
print('[STARTING] server is starting...')
start()