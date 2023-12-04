import socket

class Server:
    def __init__(self, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(("localhost", port))
        self.port = port
        self.client_socket = None
        self.client_address = None
        self.server_turn = False
        self.client_turn = True


    def start(self):
        self.server.listen(1)
        print("Server listening on port {}".format(self.port))

        self.client_socket, self.client_address = self.server.accept()
        print("Connection from {}".format(self.client_address))

    def handle_client(self):
        try:
            while True:
                if self.client_turn:
                    data = self.recvData()
                    if data:
                        print("Client: {}".format(data))
                        self.server_turn = True
                        self.client_turn = False
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

    def recvData(self):
        return self.client_socket.recv(1024).decode()
    
    def sendData(self, data):
        self.client_socket.sendall(data.encode())

    def handleSpacialCommand(self, command):
        if command == "/q" and self.server_turn:
            print("Client disconnected")
            self.handleQuitCommand()
        elif command == "/q" and self.client_turn:
            print("Server disconnected")
            self.handle_quit_command()
        elif command == "/play rock paper scissors" or command == "/play rps" or command == "/play rockpaperscissors":
            print(self.server_turn)
            print(self.client_turn)
            self.handleRockPaperScissors()
            return
        else:
            return

    def handleQuitCommand(self):
        self.client_socket.close()
        self.server.close()
        print("Server closed")
        exit() 


    def handleRockPaperScissors(self):
        print("Starting rock paper scissors")
        winner = None
        serverScore = 0
        clientScore = 0
        while winner is None:
            if self.server_turn:
                serverChoice = input("Server choice: ")
                self.sendData(serverChoice)
                clientChoice = self.recvData()
                self.handleSpacialCommand(clientChoice)
                self.handleSpacialCommand(serverChoice)
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
            print("Server score: {} Client score: {}".format(serverScore, clientScore))
            if serverScore == 3:
                winner = "Server"
            elif clientScore == 3:
                winner = "Client"
        if self.server_turn:
            self.sendData("The winner is: {}".format(winner))
            self.client_turn = True
            self.server_turn = False
        elif self.client_turn:
            self.recvData()
            self.sendData("The winner is: {}".format(winner))
            self.client_turn = True
            self.server_turn = False



if __name__ == "__main__":
    port = 12345
    server = Server(port)
    server.start()
    server.handle_client()

