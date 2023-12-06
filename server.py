import socket


'''
Name: Server
Description: Server class that handles the connection to the client and
sending and receiving data
'''


class Server:
    def __init__(self, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(("localhost", port))
        self.port = port
        self.client_socket = None
        self.client_address = None
        self.server_turn = False
        self.client_turn = True

    '''
    Name: start
    Description: Starts the server, listens for a connection, and accepts
    the connection
    additionally prints out instructions for the user
    '''
    def start(self):
        # Listen for 1 connection
        self.server.listen(1)
        print("Server listening on port {}".format(self.port))
        # Accept connection
        self.client_socket, self.client_address = self.server.accept()
        print("Connection from {}".format(self.client_address))
        print("Enter message to send to client, "
              "Wait for input prompt before starting")
        print("Enter /q to quit")
        print("Enter /play rock paper scissors or /play "
              "rps to play rock paper scissors")

    '''
    Name: handle_client
    Description: Handles the client, receives data from the client,
    and sends data to the client
    '''
    def handle_client(self):
        try:
            while True:
                # If it's the client's turn
                if self.client_turn:
                    # Receive data from client
                    data = self.recvData()
                    if data:
                        # Print message from client
                        print("Client: {}".format(data))
                        # update Turns
                        self.server_turn = True
                        self.client_turn = False
                        # check for special commands
                        self.handleSpacialCommand(data)
                elif self.server_turn:
                    reply = input("Enter your reply: ")
                    self.sendData(reply)
                    self.server_turn = False
                    self.client_turn = True
                    self.handleSpacialCommand(reply)

        except Exception as e:
            print("Error: {}".format(e))
        finally:
            self.client_socket.close()

    '''
    Name: recvData
    Description: Receives data from the client
    '''
    def recvData(self):
        return self.client_socket.recv(4096).decode()

    '''
    Name: sendData
    Description: Sends data to the client
    '''
    def sendData(self, data):
        self.client_socket.sendall(data.encode())

    '''
    Name: handleSpacialCommand
    Description: Handles special commands, such as /q to quit,
    and /play rock paper scissors
    '''
    def handleSpacialCommand(self, command):
        # if /q is detected
        if command == "/q" and self.server_turn:
            print("Client disconnected")
            self.handleQuitCommand()
        elif command == "/q" and self.client_turn:
            print("Server disconnected")
            self.handleQuitCommand()
        # if /play rock paper scissors is detected
        elif (command == "/play rock paper scissors" or
              command == "/play rps" or command == "/play rockpaperscissors"):
            self.handleRockPaperScissors()
            return
        else:
            return

    '''
    Name: handleQuitCommand
    Description: Handles the /q command, closes the server, and exits
    the program
    '''
    def handleQuitCommand(self):
        self.client_socket.close()
        self.server.close()
        print("Server closed")
        exit()

    '''
    Name: handleRockPaperScissors
    Description: Handles the rock paper scissors game, sends and receives data
    from the client
    and determines the winner of the game
    '''
    def handleRockPaperScissors(self):
        print("Starting rock paper scissors")
        winner = None
        serverScore = 0
        clientScore = 0
        while winner is None:
            # if it's the server's turn at the start of the game
            if self.server_turn:
                serverChoice = input("Server choice: ")
                self.sendData(serverChoice)
                clientChoice = self.recvData()
                self.handleSpacialCommand(clientChoice)
                self.handleSpacialCommand(serverChoice)
            # if it's the client's turn at the start of the game
            elif self.client_turn:
                clientChoice = self.recvData()
                self.handleSpacialCommand(clientChoice)
                serverChoice = input("Server choice: ")
                self.sendData(serverChoice)
                self.handleSpacialCommand(clientChoice)
                self.handleSpacialCommand(serverChoice)
            serverChoice = serverChoice.lower()
            clientChoice = clientChoice.lower()
            print("Client choice: {}".format(clientChoice))
            if serverChoice == clientChoice:
                print("Draw")
            elif serverChoice == "rock" and clientChoice == "paper":
                print("Client wins")
                clientScore += 1
            elif serverChoice == "rock" and clientChoice == "scissors":
                print("Server wins")
                serverScore += 1
            elif serverChoice == "paper" and clientChoice == "rock":
                print("Server wins")
                serverScore += 1
            elif serverChoice == "paper" and clientChoice == "scissors":
                print("Client wins")
                clientScore += 1
            elif serverChoice == "scissors" and clientChoice == "rock":
                print("Client wins")
                clientScore += 1
            elif serverChoice == "scissors" and clientChoice == "paper":
                print("Server wins")
                serverScore += 1
            print("Server score: {} Client score: {}".format(serverScore,
                                                             clientScore))
            if serverScore == 3:
                winner = "Server"
            elif clientScore == 3:
                winner = "Client"
        if self.server_turn:
            self.sendData("The winner is: {}".format(winner))
            self.client_turn = True
            self.server_turn = False

        elif self.client_turn:
            # recv data to resolve turn issue
            self.recvData()
            self.sendData("The winner is: {}".format(winner))
            self.client_turn = True
            self.server_turn = False


if __name__ == "__main__":
    port = 12345
    server = Server(port)
    server.start()
    server.handle_client()
