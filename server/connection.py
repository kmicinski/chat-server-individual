from threading import Thread
from parser import *
from messages import *

class Connection(Thread):
    """Connections object represent a single client connected to the server"""
    def __init__(self,conn,state):
        Thread.__init__(self)
        self.parser = Parser()
        self.conn = conn
        self.PACKET_LENGTH = 1024
        self.state = state

    def run(self):
        print("Initiated connection to a client!!!")
        print("Now I just have to do the rest :(")
        while true:
            data = self.conn.recv(self.PACKET_LENGTH)
            # Do something with the data here..
