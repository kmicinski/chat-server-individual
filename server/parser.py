from messages import *

class Parser():
    """Parser for messages sent via the SquirrelChat protocol"""
    def __init__(self):
        self.current_input = ""

    # Parse a simple packet
    def parse_packet(self,data):
        string = data.decode("utf-8")
        split = string.split()
        if split[0] == "authenticate":
            return AuthenticateCommand(split[1],split[2])
        elif split[0] == "register":
            return RegisterCommand(split[1],split[2])
        elif split[0] == "chat":
            msg = string.split(' ', 2)
            return ChatCommand(msg[1],msg[2])
        elif split[0] == "error":
            msg = string.split(' ', 1)
            return ErrorMessage(msg[0],msg[1])
        elif split[0] == "join":
            return JoinCommand(split[1])
        elif split[0] == "topic":
            return TopicMessage(split[1],string.split(2)[2])
        else:
            raise Exception("Could not parse packet")
