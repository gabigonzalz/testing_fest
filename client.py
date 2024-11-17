import socket
import threading
from simple_chalk import chalk
import sys

COLORS = ["black" , "red", "green", "yellow", "blue", "magenta", "cyan", "white"]

def color_checker(nick):
    print(f"Colors available: {', '.join(COLORS)}")

    for attempt in range(3):
        color = input("Choose a color: ").strip().lower()
        
        # Check if color is valid or if input is empty
        if color == "":
            nickname = chalk.white(nick)
            return nickname
        elif color in COLORS:
            nickname = getattr(chalk, color)(nick)  # Use chalk to apply the color
            return nickname
        else:
            print(f"Invalid color '{color}', please choose from the list.")
    
    # If the user failed to select a valid color, exit
    print("Failed to choose a valid color. Closing the program...")
    sys.exit(0)


# Function to receive messages
def receive():
    while True:
        # Try to receive messages from the server
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':  # If the server requests our nickname
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        # If there was an error receiving messages, close the connection
        except:
            print("An error occurred!")
            client.close()
            break

# Function to send messages
def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('utf-8'))
        
if __name__ == "__main__":
    print("""
        ##################################################################
            █▀ █▀█ █▀▀ █▄▀   █ ▀█▀   ▀█▀ █▀█   █▀▄▀█ █▀▀   █▀▀ █░█ ▄▀█ ▀█▀
            ▄█ █▄█ █▄▄ █░█   █ ░█░   ░█░ █▄█   █░▀░█ ██▄   █▄▄ █▀█ █▀█ ░█░
        ##################################################################
        """)

    nick = input("Enter your nickname: ")

    nickname = color_checker(nick)

    # Connect to the server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(('127.0.0.1', 55555))
        print("Connected to the server")
        
    # If there was a connection error
    except ConnectionRefusedError:
        print("Could not connect to the server. Make sure the server is online")
        exit()

    # Create threads for receiving and writing functions
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()
