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
                    self.handle_quit_command(data)
                    print("Client: {}".format(data))
                    reply = input("Enter your reply: ")
                    self.handle_quit_command(reply)
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

    def handleQuitCommand(self):
        self.client_socket.close()
        self.server.close()
        print("Server closed")
        exit() 


    def handleRockPaperScissors(self):
        pass

