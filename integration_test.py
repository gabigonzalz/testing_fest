import pytest
import socket
import threading
import time
import select

HOST = '127.0.0.1'  # Server host address
PORT = 55555  # Port for server communication

class ClientThread(threading.Thread):
    """
    Represents a client in the chat system, which runs on a separate thread.
    Each client connects to the server, sends and receives messages.
    """
    def __init__(self, nickname, event):
        super().__init__()
        self.nickname = nickname  # Client's nickname
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creating the socket for communication
        self.received_messages = []  # List to store messages received by the client
        self.running = True  # Flag to control the client's running state
        self.event = event  # Event used for synchronizing when the client is ready

    def run(self):
        """Main loop where the client connects to the server and listens for incoming messages."""
        try:
            # Connect to the server
            self.client.connect((HOST, PORT))
            # Wait for the server to prompt for a nickname
            self.client.recv(1024)  # Receive the 'NICK' prompt
            # Send the nickname to the server
            self.client.send(self.nickname.encode('utf-8'))
            # Signal that the client is ready to receive messages
            self.event.set()

            # Keep running and listening for incoming messages
            while self.running:
                # Use select to check for readable messages (non-blocking)
                readable, writable, exceptional = select.select([self.client], [], [], 1)
                if readable:
                    # Receive and decode the message
                    message = self.client.recv(1024).decode('utf-8')
                    if message:
                        # Append the received message to the list
                        self.received_messages.append(message)

        except OSError:
            # If an error occurs (e.g., the connection is closed), stop the client
            pass

    def send_message(self, message):
        """Sends a message to the server."""
        try:
            # Send the message to the server
            self.client.send(message.encode('utf-8'))
        except socket.error:
            # Handle socket errors (e.g., server not reachable)
            pass

    def stop(self):
        """Stops the client and closes the connection."""
        self.running = False
        self.client.close()

@pytest.fixture
def multiple_clients():
    """
    Fixture to start multiple clients for testing.
    It initializes multiple `ClientThread` instances and synchronizes their start.
    """
    event = threading.Event()  # Create a threading event for synchronization
    clients = [ClientThread(f"Client{i}", event) for i in range(3)]  # Create 3 clients with different nicknames
    for client in clients:
        client.start()  # Start each client in a separate thread

    # Wait until all clients are connected and ready
    event.wait()  # Ensure all clients are connected to the server

    yield clients  # Provide the clients to the test
    for client in clients:
        # Stop each client after the test is done
        client.stop()
        client.join()  # Wait for each client thread to finish

# Test with synchronization using Event
def test_message_distribution(multiple_clients):
    """
    Verifies that when one client sends a message, the other clients receive it.
    This ensures proper message distribution in the chat system.
    """
    clients = multiple_clients

    # Create events for synchronization so clients can be ready at the same time
    events = [client.event for client in clients]
    for event in events:
        event.wait()  # Wait until all clients are ready

    # Client 0 sends a message
    test_message = "Hello from Client0"
    clients[0].send_message(test_message)
    time.sleep(1)  # Wait a short time for clients to receive the message

    # Check if the other clients received the message
    for i, client in enumerate(clients[1:], start=1):
        assert any(test_message in msg for msg in client.received_messages), f"Client{i} did not receive the message."

def test_simultaneous_messaging(multiple_clients):
    """
    Test that multiple clients can send messages simultaneously,
    and that they correctly receive each other's messages (but not their own).
    """
    clients = multiple_clients
    messages = [f"Message from {client.nickname}" for client in clients]  # Prepare messages for each client

    # Create events for synchronization to ensure all clients are ready to send messages
    events = [client.event for client in clients]

    # Wait for all clients to be ready
    for event in events:
        event.wait()

    # Send messages from all clients simultaneously
    for i, client in enumerate(clients):
        client.send_message(messages[i])

    # Give clients time to receive messages
    time.sleep(3)

    # Verify that each client received messages from others, but not its own message
    for i, client in enumerate(clients):
        for j, message in enumerate(messages):
            if i != j:  # The client should not receive its own message
                assert any(message in msg for msg in client.received_messages), f"{client.nickname} did not receive {messages[j]}"

    # Ensure each client does *not* receive its own message
    for i, client in enumerate(clients):
        own_message = messages[i]
        assert all(own_message not in msg for msg in client.received_messages), f"{client.nickname} received its own message."

def test_unexpected_disconnection(multiple_clients):
    """
    Simulates the unexpected disconnection of a client and verifies that the other clients
    can still communicate properly without errors.
    """
    clients = multiple_clients

    # Disconnect client 0 to simulate an unexpected disconnection
    clients[0].stop()
    time.sleep(5)  # Give the server time to process the disconnection

    # Verify that the remaining clients can continue sending and receiving messages
    test_message = "Message after Client0 disconnect"
    clients[1].send_message(test_message)

    time.sleep(1)  # Give clients time to receive the message
    for i, client in enumerate(clients[2:], start=2):
        assert any(test_message in msg for msg in client.received_messages), f"Client{i} did not receive the message after the disconnection."
