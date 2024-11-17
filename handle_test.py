import pytest
import socket
from unittest.mock import Mock, patch
from server import handle  # Importing the 'handle' function from the server module

# Fixture to set up a mock client 
@pytest.fixture
def setup_clients_and_nicknames():
    """
    Fixture to set up a mock client with a mocked 'recv' method to simulate receiving data.
    This mock client will be used in the test cases to simulate communication between the server and the client.
    """
    client = Mock()  # Create a mock client
    client.recv = Mock()  # Mock the 'recv' method to simulate receiving data from the client
    return client  # Return the mock client to use in tests

# Test 1: Optimal case - client sends a valid message
@patch('server.nicknames', new_callable=dict)  # Mocking 'nicknames' dictionary in the server module
@patch('server.clients', new_callable=list)  # Mocking 'clients' list in the server module
@patch('server.broadcast')  # Mocking the 'broadcast' function in the server module
def test_handle_optimal(mock_broadcast, mock_clients, mock_nicknames, setup_clients_and_nicknames):
    """
    Test case where the client sends a valid message. The message should be broadcast to all other clients.
    The function should return True in this optimal case.
    """
    client = setup_clients_and_nicknames  # Set up a mock client using the fixture
    mock_clients.append(client)  # Add the mock client to the clients list
    mock_nicknames[client] = "TestUser"  # Add a nickname for the mock client
    
    # Mock the client sending a valid message
    client.recv.return_value = b'Hello, world!'  # Simulate receiving a message from the client
    
    # Call the handle function with the mock client
    result = handle(client)  # The handle function processes the message
    
    # Assertions to check the expected behavior
    mock_broadcast.assert_called_once_with(b'Hello, world!', client)  # Ensure the broadcast function is called with the correct message
    assert result is True  # Ensure the handle function returns True (indicating a successful operation)

# Test 2: Client exits gracefully (no message sent)
@patch('server.nicknames', new_callable=dict)  # Mocking 'nicknames' dictionary in the server module
@patch('server.clients', new_callable=list)  # Mocking 'clients' list in the server module
@patch('server.broadcast')  # Mocking the 'broadcast' function in the server module
def test_handle_client_exit(mock_broadcast, mock_clients, mock_nicknames, setup_clients_and_nicknames):
    """
    Test case where the client disconnects (sends an empty message). This simulates a graceful exit.
    The function should broadcast a message indicating the client has left the chat.
    """
    client = setup_clients_and_nicknames  # Set up a mock client using the fixture
    mock_clients.append(client)  # Add the mock client to the clients list
    mock_nicknames[client] = "TestUser"  # Add a nickname for the mock client
    
    # Simulate the client sending no message (disconnection)
    client.recv.return_value = b''  # Simulate an empty message indicating client exit
    
    # Call the handle function
    result = handle(client)  # The handle function should handle the disconnection
    
    # Assertions to verify the expected behavior
    mock_broadcast.assert_called_once_with("TestUser left the chat.".encode('utf-8'))  # Ensure the exit message is broadcasted
    assert result is False  # The function should return False when the client exits gracefully

# Test 3: Client encounters a socket error
@patch('server.nicknames', new_callable=dict)  # Mocking 'nicknames' dictionary in the server module
@patch('server.clients', new_callable=list)  # Mocking 'clients' list in the server module
@patch('server.broadcast')  # Mocking the 'broadcast' function in the server module
def test_handle_socket_error(mock_broadcast, mock_clients, mock_nicknames, setup_clients_and_nicknames):
    """
    Test case where the client encounters a socket error while receiving data.
    The function should not broadcast any message and should return False due to the error.
    """
    client = setup_clients_and_nicknames  # Set up a mock client using the fixture
    mock_clients.append(client)  # Add the mock client to the clients list
    mock_nicknames[client] = "TestUser"  # Add a nickname for the mock client
    
    # Simulate a socket error during data reception
    client.recv.side_effect = socket.error("Socket error during recv")  # Raise a socket error when trying to recv
    
    # Call the handle function
    result = handle(client)  # The handle function should handle the error
    
    # Assertions to verify the expected behavior
    mock_broadcast.assert_not_called()  # Ensure that no broadcast happens when there's a socket error
    assert result is False  # The function should return False due to the socket error

# Test 4: Client sends a message that is too long
@patch('server.nicknames', new_callable=dict)  # Mocking 'nicknames' dictionary in the server module
@patch('server.clients', new_callable=list)  # Mocking 'clients' list in the server module
@patch('server.broadcast')  # Mocking the 'broadcast' function in the server module
def test_handle_long_message(mock_broadcast, mock_clients, mock_nicknames, setup_clients_and_nicknames):
    """
    Test case where the client sends a message that is too long (e.g., longer than the allowed size).
    The function should not broadcast the message and should return False.
    """
    client = setup_clients_and_nicknames  # Set up a mock client using the fixture
    mock_clients.append(client)  # Add the mock client to the clients list
    mock_nicknames[client] = "TestUser"  # Add a nickname for the mock client
    
    # Mock the client sending a message that exceeds the allowed length (e.g., 2048 bytes)
    long_message = b'A' * 2048  # Simulate a message longer than 1024 bytes (limit)
    client.recv.return_value = long_message  # Simulate receiving a long message
    
    # Call the handle function
    result = handle(client)  # The handle function should handle the long message case
    
    # Assertions to verify the expected behavior
    mock_broadcast.assert_not_called()  # Ensure no broadcast happens for a long message
    assert result is False  # The function should return False for long messages
