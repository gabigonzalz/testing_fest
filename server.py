import socket
import select
import time

# Configure the addresses
HOST = '127.0.0.1'  # localhost
PORT = 55555 

# Define the type of connection and protocol
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Configure the host and port to be reusable
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Apply the configurations to the server and start it
server.bind((HOST, PORT))
server.listen(100)

# Create lists for clients/nicknames
clients = [server]
nicknames = {}

# Function to remove and disconnect clients
def remove(client):
    if client in clients:
        clients.remove(client)
    if client in nicknames:
        print(f"Client {nicknames[client]} has disconnected")
        del nicknames[client]
    client.close()

# Broadcast messages to all clients (announcement)
def broadcast(message, sender=None):
    # List of problematic clients
    clients_to_remove = []
    
    for client in clients:
        if client != sender and client != server:
            
            # Try to send a message
            for attempt in range(3):
                try:
                    print(f"Trying to send message: {message}")
                    client.send(message)
                    break
                
                except socket.error as error:
                    print(f"Error sending message to a client: {error}\n        Retrying: {attempt+1}...")
                    time.sleep(1)  # Wait before retrying
            
            # If, after 3 attempts, it still doesn't work
            else:
                clients_to_remove.append(client)
    
    # Remove problematic clients
    for client in clients_to_remove:
        remove(client)
        broadcast(f"{nicknames.get(client, 'Unknown')} left the chat.".encode('utf-8'))

# Handle message receiving and transmission from a client
def handle(client):
    for attempt in range(3):
        
        # Try to receive a message
        try:
            message = client.recv(1024)
            if message:
                print(f"received message trying to broadcast: {message}")
                broadcast(message, client)
                return True
            
            else:
                # Client exited cleanly
                broadcast(f"{nicknames.get(client, 'Unknown')} left the chat.".encode('utf-8'))
                return False
            
        except socket.error as error:
            print(f"Error receiving data from a client: {error}\n        Retrying: {attempt+1}...")
            time.sleep(1)
            
    return False

# Accept new connections
def accept(server):
    client, address = server.accept()
    print(f"Address {str(address)} connected")

    # Request the client's nickname
    client.send('NICK'.encode('utf-8'))
    nickname = client.recv(1024).decode('utf-8')
    nicknames[client] = nickname
    clients.append(client)

    # Announce the new connection
    print(f"The client's nickname is '{nickname}'.")
    broadcast(f"{nickname} joined the chat".encode('utf-8'), client)

if __name__ == "__main__":
    print("""
        #######################################################################
        #                        SERVER ONLINE                                #
        #######################################################################
        """)

    print(f"-> Server listening on {HOST}:{PORT}")


    while True:
        
        # Use select to monitor sockets
        read_sockets, write_sockets, exception_sockets = select.select(clients, [], clients)  # read, write, exceptions (error)

        # For each socket ready to read
        for sock in read_sockets:

            if sock == server:
                accept(server)
            
            else:
                # Try to receive/transmit
                if not handle(sock):
                    remove(sock)
        
        # For each socket with errors
        for sock in exception_sockets:
            remove(sock)
