import pytest
from unittest.mock import Mock, patch
from server import remove  # Importing the 'remove' function from the server module

# Mock data for testing
@pytest.fixture
def setup_clients_and_nicknames():
    """
    Fixture to create a mock client with a mocked 'close' method.
    This mock will simulate a client object that can be used in the tests.
    """
    client = Mock()  # Create a mock client
    client.close = Mock()  # Mock the 'close' method of the client
    return client  # Return the mock client for use in the tests

# Test 1: Optimal case - successful removal of a client
@patch('server.nicknames', new_callable=dict)  # Mocking 'nicknames' dictionary in the server module
@patch('server.clients', new_callable=list)  # Mocking 'clients' list in the server module
def test_remove_optimal(mock_clients, mock_nicknames, setup_clients_and_nicknames):
    """
    Test case for the optimal scenario where a valid client is removed successfully from both
    the clients list and the nicknames dictionary.
    """
    client = setup_clients_and_nicknames  # Set up a mock client using the fixture
    mock_clients.append(client)  # Add the client to the mock clients list
    mock_nicknames[client] = "TestUser"  # Add the client's nickname to the mock nicknames dictionary
    
    # Patch the 'clients' and 'nicknames' in the server module, then call 'remove'
    with patch('server.clients', mock_clients), patch('server.nicknames', mock_nicknames):
        remove(client)  # Call the remove function to simulate client removal
    
    # Assertions to verify the correct behavior
    assert client not in mock_clients  # Ensure the client is removed from the clients list
    assert client not in mock_nicknames  # Ensure the client's nickname is removed from the nicknames dictionary
    client.close.assert_called_once()  # Ensure that the 'close' method of the client is called once

# Test 2: Invalid client case - client is an empty string
@patch('server.nicknames', new_callable=dict)  # Mocking 'nicknames' dictionary in the server module
@patch('server.clients', new_callable=list)  # Mocking 'clients' list in the server module
def test_no_client(mock_clients, mock_nicknames):
    """
    Test case where the client passed to the 'remove' function is an empty string, which is invalid.
    The function should raise a ValueError.
    """
    with pytest.raises(ValueError):  # Expecting a ValueError when passing an invalid client
        with patch('server.clients', mock_clients), patch('server.nicknames', mock_nicknames):
            remove("")  # Calling remove with an empty string as the client

# Test 3: Client not found in either clients or nicknames
@patch('server.nicknames', new_callable=dict)  # Mocking 'nicknames' dictionary in the server module
@patch('server.clients', new_callable=list)  # Mocking 'clients' list in the server module
def test_wrong_client(mock_clients, mock_nicknames, setup_clients_and_nicknames):
    """
    Test case where the client passed to 'remove' does not exist in the 'clients' or 'nicknames'.
    The original client should not be removed.
    """
    client = setup_clients_and_nicknames  # Set up a mock client using the fixture
    fake_client = Mock()  # Create another mock client (which does not exist in the clients list)

    # Add the real client to the mock clients list and nicknames dictionary
    mock_clients.append(client)
    mock_nicknames[client] = "TestUser"
    
    # Patch the 'clients' and 'nicknames' in the server module, then call 'remove' with a fake client
    with patch('server.clients', mock_clients), patch('server.nicknames', mock_nicknames):
        remove(fake_client)  # Attempt to remove a non-existent client
    
    # Assertions to verify the original client was not affected
    assert client in mock_clients  # The real client should still be in the clients list
    assert mock_nicknames[client] == "TestUser"  # The nickname of the real client should still be "TestUser"
