import socket
import random
import threading
import sys

BOARD_SIZE = 100
LADDERS = {3: 22, 5: 8, 11: 26, 20: 29, 17: 4, 19: 7}
SNAKES = {27: 1, 21: 9, 25: 3, 34: 5, 32: 30, 99: 78}
PORT = 12343

# Player class to manage each player's position
class Player:
    def __init__(self, name):
        self.name = name
        self.position = 0

    def move(self, steps):
        if self.position + steps <= BOARD_SIZE:
            self.position += steps
        self.position = self.check_snakes_ladders(self.position)
        return self.position

    def check_snakes_ladders(self, pos):
        if pos in LADDERS:
            print(f"Ladder! {self.name} climbs from {pos} to {LADDERS[pos]}")
            return LADDERS[pos]
        elif pos in SNAKES:
            print(f"Snake! {self.name} slides from {pos} to {SNAKES[pos]}")
            return SNAKES[pos]
        return pos

def roll_dice():
    return random.randint(1, 6)

# Master server handling the game logic
def master_game(num_players):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', PORT))
    server_socket.listen(num_players)
    print("Master: Waiting for players to connect...")

    players = []
    client_sockets = []

    # Accept connections from slaves
    for i in range(num_players-1):
        client_socket, address = server_socket.accept()
        print(f"Player {i+1} connected from {address}")
        player = Player(f"Player {i+1}")
        players.append(player)
        client_sockets.append(client_socket)

    players.append(Player(f"Player {num_players}"))
    winner = None
    turn = 0

    # Game loop
    while not winner:
        current_player = players[turn]
        if(turn == num_players-1):
            dice_value = roll_dice()
            print(f"{current_player.name} rolled a {dice_value}")

            new_position = current_player.move(dice_value)
            print(f"{current_player.name} moved to {new_position}")

            if new_position == BOARD_SIZE:
                winner = current_player.name
                break

            turn = (turn + 1) % num_players
            continue
        
        current_socket = client_sockets[turn]

        # Request dice roll from current player
        current_socket.sendall(b'ROLL')
        dice_value = int(current_socket.recv(1024).decode())
        print(f"{current_player.name} rolled a {dice_value}")

        new_position = current_player.move(dice_value)
        print(f"{current_player.name} moved to {new_position}")

        # Check if this player has won
        if new_position == BOARD_SIZE:
            winner = current_player.name
            break

        turn = (turn + 1) % num_players

    print(f"{winner} wins the game!")
    for sock in client_sockets:
        sock.sendall(f"{winner} wins!".encode())
    server_socket.close()


# Slave client that connects to master and rolls dice
def slave_player():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', PORT))
    print("Slave: Connected to master.")

    while True:
        message = client_socket.recv(1024).decode()
        if message == 'ROLL':
            dice_value = roll_dice()
            print(f"Rolled dice: {dice_value}")
            client_socket.sendall(str(dice_value).encode())
        elif "wins" in message:
            print(message)
            break
    client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python player.py [master/slave]")
        sys.exit(1)
    
    role = sys.argv[1].lower()
    
    if role == 'master':
        players = int(input("Enter the number of players (2-4): "))
        if players < 2 or players > 4:
            print("Invalid number of players. Must be between 2 and 4.")
            sys.exit(1)
        master_game(players)
    
    elif role == 'slave':
        slave_player()
    
    else:
        print("Invalid argument. Use 'master' or 'slave'.")