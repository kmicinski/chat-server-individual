from connection import *
from socket import *
from state import *

class Server:
    """Toplevel server implementation"""
    
    def run(self):
        s = socket(AF_INET, SOCK_STREAM)
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        s.bind((gethostbyname("localhost"),self.port))
        s.listen(5)
        while 1:
            print("Waiting for new connections..")
            (client,address) = s.accept()
            connection = Connection(client,self.state)
            print("Running thread for connection..")
            connection.start()

    def __init__(self,port):
        self.port = port
        self.state = State()

print("Note that I am currently ignoring the passwords file!")

# Main code entry: build a server and start it
s = Server(4000)
s.run()
