#####################################################
### Team Members: Akshad Vivek Gajbhiye (2203101) ###
###               Ishita Partha Chail   (2203107) ###
#####################################################

import socket
import random

SERVER_IP = '127.0.0.1'     # Replace with your server's IP address
PORT = 65431                # Port to send request to

# Function to randomly roll a dice
def rollDice():
    return random.randint(1,6)

# Parameters for colours in terminal
colours = {'1':"\033[31m", '2':"\033[32m", '3':"\033[33m", '4':"\033[34m"}
reset = "\033[0m"

# Connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, PORT))
message = client_socket.recv(1024).decode()
if message=="Enter your board number: ":
    boardNum = int(input(message))
    client_socket.sendall(f"{boardNum}".encode())

start = client_socket.recv(1024).decode()
print(start)

# Run this until the game ends
while True:
    message = client_socket.recv(1024).decode()
    if message == "ROLL":
        num = rollDice()
        print(f"You rolled {num}")
        client_socket.sendall(f"{num}".encode())
    elif message == "END":
        break
    else:
        print(colours[message[7]]+message+reset)