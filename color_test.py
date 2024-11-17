from client import color_checker  # Import the function to be tested
import pytest  # Pytest is used for testing
from unittest.mock import patch  # To mock built-in functions like `input`
import sys  # For handling system exit in tests

# Test 1: User chooses a valid color
def test_valid_color(): # HAPPY PATH
    """
    This test case simulates a scenario where the user provides a valid color 
    ('blue') through input, and the color_checker function should return the 
    nickname with blue color (using ANSI escape codes).
    """
    with patch('builtins.input', return_value='blue'):  # Mocking user input to return 'blue'
        result = color_checker("TestUser")  # Call the function with a sample username
        # Assert that the result matches the ANSI escape code for blue color
        assert result == '\x1b[34mTestUser\x1b[0m' # (blue color for the text)

# Test 2: User chooses an empty string (should default to 'white')
def test_empty_string_color(): # EDGE CASE
    """
    This test case simulates a scenario where the user provides an empty string 
    as input. The function should default to 'white' if no valid color is chosen.
    """
    with patch('builtins.input', return_value=''):  # Mocking user input as an empty string
        result = color_checker("TestUser")  # Call the function with a sample username
        # Assert that the result matches the ANSI escape code for white color
        assert result == '\x1b[37mTestUser\x1b[0m' # (white color for the text)

# Test 3: User provides an invalid color three times
def test_invalid_colors(): # ERROR CASE
    """
    This test case simulates a scenario where the user repeatedly enters invalid 
    color options ('purple', 'orange', 'pink'). The function should raise a SystemExit 
    after three invalid attempts.
    """
    with patch('builtins.input', side_effect=['purple', 'orange', 'pink']):  # Mocking invalid inputs
        with pytest.raises(SystemExit):  # Expecting a system exit after 3 invalid attempts
            color_checker("TestUser")  # Call the function with a sample username

# Test 4: User chooses a valid color after one invalid attempt
def test_invalid_then_valid_color(): # RECOVERY CASE
    """
    This test case simulates a scenario where the user provides an invalid color 
    ('purple') initially, followed by a valid color ('red'). The function should 
    apply the valid color ('red') after one invalid attempt.
    """
    with patch('builtins.input', side_effect=['purple', 'red']):  # Mocking first invalid, then valid input
        result = color_checker("TestUser")  # Call the function with a sample username
        # Assert that the result matches the ANSI escape code for red color
        assert result == '\x1b[31mTestUser\x1b[0m' # (red color for the text)
