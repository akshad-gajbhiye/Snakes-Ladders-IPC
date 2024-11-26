#####################################################
### Team Members: Akshad Vivek Gajbhiye (2203101) ###
###               Ishita Partha Chail   (2203107) ###
#####################################################

import socket
import threading
import time

# Dictionary to track clients grouped by game codes
players = {}

# Lock for thread-safe updates to the `players` dictionary
lock = threading.Lock()

# Server configuration
HOST = '127.0.0.1'  # Localhost
PORT = 65431        # Port to listen on

# Parameters for colours in terminal
colours = ["\033[31m", "\033[32m", "\033[33m", "\033[34m", "\033[35m", "\033[36m"]
reset = "\033[0m"
col = 0

# Class of Board Game which will track every players' position, snakes and ladders
class BoardGame:
    def __init__(self):
        # Initialize board, players, snakes, and ladders
        self.boardNum = 0
        self.boardCol = 0
        self.board_size = 100  # Board from 1 to 100
        self.players = {1: 0, 2: 0, 3: 0, 4: 0}  # Player positions start at 0
        self.snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
        self.ladders = {2: 38, 7: 14, 8: 31, 15: 26, 28: 84, 21: 42, 36: 44, 51: 67, 71: 91, 78: 98, 87: 94}

    # Function to move the player based on dice roll and handle snakes/ladders
    def move_player(self, player, steps):
        current_position = self.players[player]
        new_position = current_position + steps

        if new_position > self.board_size:
            print(f"{colours[self.boardCol]}Game Room {self.boardNum}{reset}: ", end="")
            print(f"Player {player} rolls {steps} but stays at position {current_position} (overshoots the board).")
            return  # Do not move if the position exceeds board size
        
        print(f"{colours[self.boardCol]}Game Room {self.boardNum}{reset}: ", end="")
        print(f"Player {player} moves from {current_position} to {new_position}.")
        
        # Check for snakes or ladders
        if new_position in self.snakes:
            print(f"{colours[self.boardCol]}Game Room {self.boardNum}{reset}: ", end="")
            print(f"Oops! Player {player} bitten by a snake at {new_position}. Goes down to {self.snakes[new_position]}.")
            new_position = self.snakes[new_position]
        elif new_position in self.ladders:
            print(f"{colours[self.boardCol]}Game Room {self.boardNum}{reset}: ", end="")
            print(f"Yay! Player {player} climbs a ladder at {new_position}. Goes up to {self.ladders[new_position]}.")
            new_position = self.ladders[new_position]

        self.players[player] = new_position
        print(f"{colours[self.boardCol]}Game Room {self.boardNum}{reset}: ", end="")
        print(f"Player {player} is now at position {new_position}.")

    # Function to check if the player has won
    def is_winner(self, player):
        return self.players[player] == self.board_size

# Function to handle a game with 4 players
def handle_game(game_code):
    print(f"Starting a new game for board number {game_code} with 4 players.")
    player_sockets = players[game_code]
    players[game_code] = []
    
    # Below 5 lines are to give a unique colour to a board
    global col
    game = BoardGame()
    game.boardNum = game_code
    game.boardCol = col
    col=(col+1)%6

    # Notify players that the game is starting
    for i, client in enumerate(player_sockets):
        try:
            client.sendall(f"Game starting for board {colours[game.boardCol]}{game_code}{reset}. You are Player {i + 1}.".encode('utf-8'))
        except Exception as e:
            print(f"Error communicating with Player {i + 1}: {e}")
    
    while True:
        for i, client in enumerate(player_sockets):
            time.sleep(0.3)
            client.sendall("ROLL".encode())  # Sending message to roll the dice
            dice_value = int(client.recv(1024).decode())  # Receiving dice value
            print(f"{colours[game.boardCol]}Game Room {game.boardNum}{reset}: ", end="")
            print(f"Player {i+1} rolled a {dice_value}")

            game.move_player(i+1,dice_value)

            # Sending new player positions to all
            for sock in player_sockets:
                sock.sendall(f"Player {i+1} rolled {dice_value} and new positions are {game.players}".encode())

            # Stop the game is a player wins
            if(game.is_winner(i+1)):
                for sock in player_sockets:
                    sock.sendall(f"Player {i+1} won the game".encode())
                    time.sleep(1)
                    sock.sendall("END".encode())
                return
    
    # Close connections after the game
    for client in player_sockets:
        client.close()

    print(f"Game for board {game_code} ended and connections closed.")

# Function to handle a client
def handle_client(client_socket, client_address):
    try:
        client_socket.sendall("Enter your board number: ".encode('utf-8'))
        board_number = client_socket.recv(1024).decode('utf-8').strip()

        if not board_number.isdigit():
            client_socket.sendall("Invalid board number. Connection closing.".encode('utf-8'))
            client_socket.close()
            return

        print(f"Client {client_address} joined board {board_number}.")
        
        # If board number is not in players dictionary then add it
        with lock:
            if board_number not in players:
                players[board_number] = []
            players[board_number].append(client_socket)
        
        # Check if there are 4 players for this board number, if yes then start the game in another thread
        if len(players[board_number]) == 4:
            # Starting game in a new thread
            game_thread = threading.Thread(target=handle_game, args=(board_number,))
            game_thread.start()

    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
        client_socket.close()

# Function will use threading to get new clients and handle a client
def start_server():
    """Start the server and accept client connections."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(50)  # Allow up to 50 pending connections
    print(f"Server started on {HOST}:{PORT} and waiting for connections...")

    try:
        # Listening to clients
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"New connection from {client_address}.")
            # Creating a thread to handle the client
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        server_socket.close()

# Starting the server
if __name__ == "__main__":
    start_server()