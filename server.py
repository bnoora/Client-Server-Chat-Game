import socket

class Server:
    def __init__(self, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(("localhost", port))
        self.port = port
        self.client_socket = None
        self.client_address = None


    def start(self):
        self.server.listen(1)
        print("Server listening on port {}".format(self.port))

        self.client_socket, self.client_address = self.server.accept()
        print("Connection from {}".format(self.client_address))

    def handle_client(self):
        try:
            while True:
                data = self.client_socket.recv(1024).decode()
                if data:
                    self.handleSpacialCommand(data)
                    print("Client: {}".format(data))
                    reply = input("Enter your reply: ")
                    self.handleSpacialCommand(reply)
                    self.client_socket.sendall(reply.encode())
        except:
            print("Error: Client disconnected")
        finally:
            self.client_socket.close()


    def handleSpacialCommand(self, command):
        if command == "/q":
            self.handle_quit_command()
        elif command == "/play rock paper scissors" or command == "/play rps" or command == "/play rockpaperscissors":
            self.handle_rock_paper_scissors()
        else:
            return

    def handleQuitCommand(self):
        self.client_socket.close()
        self.server.close()
        print("Server closed")
        exit() 


    def handleRockPaperScissors(self):
        winner = None
        serverScore = 0
        clientScore = 0
        while winner is None:
            serverChoice = input("Server choice: ")
            clientChoice = self.client_socket.recv(1024).decode()
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
        print("{} wins".format(winner))


