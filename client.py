import socket

class Client:
    def __init__(self, host, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.server_turn = False
        self.client_turn = True

    def connect(self):
        try:
            self.client.connect((self.host, self.port))
            print("Connected to server on {}:{}".format(self.host, self.port))
        except Exception as e:
            print("Failed to connect to server: {}".format(e))
            exit()

    def start(self):
        try:
            while True:
                if self.client_turn:
                    message = input("Enter your message: ")
                    self.sendData(message)
                    self.client_turn = False
                    self.server_turn = True
                    self.handleSpacialCommand(message)
                elif self.server_turn:
                    reply = self.recvData()
                    print("Server: {}".format(reply))
                    self.server_turn = False
                    self.client_turn = True
                    self.handleSpacialCommand(reply)

        except Exception as e:
            print("Error: {}".format(e))
        finally:
            self.client.close()

    def recvData(self):
        return self.client.recv(1024).decode()

    def sendData(self, data):
        self.client.sendall(data.encode())

    def handleSpacialCommand(self, command):
        if command == "/q" and self.server_turn:
            print("Client disconnected")
            self.handleQuitCommand()
        elif command == "/q" and self.client_turn:
            print("Server disconnected")
            self.handleQuitCommand()
        elif command == "/play rock paper scissors" or command == "/play rps" or command == "/play rockpaperscissors":
            print(self.server_turn)
            print(self.client_turn)
            self.handleRockPaperScissors()
            return
        
    def handleQuitCommand(self):
        self.client.close()
        exit()

    def handleRockPaperScissors(self):
        print("Starting Rock Paper Scissors")
        winner = None
        serverScore = 0
        clientScore = 0
        while winner is None:
            if self.server_turn:
                serverChoice = self.recvData()
                print("Server choice: {}".format(serverChoice))
                clientChoice = input("Enter your choice: ")
                self.sendData(clientChoice)
            elif self.client_turn:
                clientChoice = input("Enter your choice: ")
                self.sendData(clientChoice)
                serverChoice = self.recvData()
                print("Server choice: {}".format(serverChoice))
            serverChoice = serverChoice.lower()
            clientChoice = clientChoice.lower()
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





# Usage
if __name__ == "__main__":
    host = "localhost" 
    port = 12345  
    client = Client(host, port)
    client.connect()
    client.start()
