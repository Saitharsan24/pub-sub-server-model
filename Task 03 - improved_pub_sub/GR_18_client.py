import socket


PORT = 9999
HOST = '192.168.56.1'
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = 'terminate'
ADDR = (HOST, PORT)


print("CLIENT_TYPE should be either 'PUBLISHER' or 'SUBSCRIBER'.")
client_type = input("Enter CLIENT_TYPE: ").upper()


while client_type not in ('PUBLISHER', 'SUBSCRIBER'):
    print("Invalid CLIENT_TYPE. Should be either 'PUBLISHER' or 'SUBSCRIBER'.")
    client_type = input("Enter CLIENT_TYPE: ").upper()
    
topic_name = input("Enter topic name: ").upper()
  

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

client.send(f"{client_type} {topic_name}".encode(FORMAT))

try:
    if client_type == 'PUBLISHER':
        while True:
            # For PUBLISHER clients, take input from the user and send it to the server
            message = input("Enter a message (type 'terminate' to exit): ")
            client.send(message.encode(FORMAT))
            if message == DISCONNECT_MESSAGE:
                break
             
    else:  # Subscriber
        while True:
            # show in terminal
            data = client.recv(1024).decode(FORMAT)
            if not data:
                break
            print(f"\nReceived from server: [TOPIC]: "+ topic_name + "\n [Message]: " + data)
    
    print("Client terminated.")
    client.close()

except KeyboardInterrupt:
        print("Connection Closed")
        client.close()
        
        
