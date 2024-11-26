# Snakes-Ladders-IPC
Files:      
     Server.py
     Player.py

How to Run the Codes: 

To run your multiplayer Snake and Ladder game on different devices, follow these steps. This assumes you have the server and player code saved in separate files, Python installed, and a network connection:

STEP 1 Set Up the Server:
-Open a terminal on the device that will act as the server.
-Navigate to the directory where server.py is located.
-Run the server using the command: python Server.py
-You should see output like:
 Server started on 127.0.0.1:65431 and waiting for connections…

STEP 2 Start the Players:
-On each player's device, open a terminal.
-Ensure the device can connect to the server. The server's IP address must be reachable (e.g., via LAN or a local network).
-For the local machine, use 127.0.0.1 as the IP.
-For different devices on the same network, use the server's local IP (find it using ipconfig on Windows or ifconfig on macOS/Linux).
-Replace 127.0.0.1 in the player code with the server's IP address.
-Navigate to the directory where player.py is located.
-Run the player code using the command: python player.py
-The player will see a prompt:
        Enter your board number:
-Enter a number (e.g., 1) to join a specific game room.

STEP 3 Add More Players:
-Repeat Step 2 for additional players. Ensure all players in the same game
   room enter the same board number.

STEP 4 Game Play:
-Once 4 players join the same board number, the server will notify all players: Game starting for board [board_number]. You are Player [X].
-Each player takes turns rolling the dice. When prompted: ROLL
-The dice will automatically roll, and the result will be displayed, e.g.: Player 1 rolled 5 and new positions are {1: 5, 2: 0, 3: 0, 4: 0}.
-The game continues until one player reaches position 100, and the server announces the winner: Player X won the game

STEP 5 End Game:
-After the game ends: all players see the message END and their connection to the server is closed.
-The server output confirms the game has ended and the connections  have been cleaned up.
