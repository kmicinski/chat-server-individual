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
            return AuthenticateMessage(split[1],split[2])
        elif split[0] == "register":
            return RegisterMessage(split[1],split[2])
        elif split[0] == "chat":
            msg = string.split(' ', 2)
            return ChatMessage(msg[1],msg[2])
        elif split[0] == "chatfrom":
            msg = string.split(' ', 3)
            return ChatFromMessage(msg[1],msg[2], msg[3])
        elif split[0] == "error":
            msg = string.split(' ', 1)
            return ErrorMessage(msg[1])
        elif split[0] == "join":
            return JoinMessage(split[1])
        elif split[0] == "topic":
            msg = string.split(' ', 2)
            return TopicMessage(msg[1],msg[2])
        elif split[0] == "update_pw":
            return UpdatePasswordMessage(split[1])
        elif split[0] == "block":
            return BlockMessage(split[1])
        elif split[0] == "ban":
            return BanMessage(split[1], split[2])
        elif split[0] == "unban":
            return UnbanMessage(split[1], split[2])
        elif split[0] == "gettopic":
            return GetTopicMessage(split[1])
        elif split[0] == "settopic":
            msg = string.split(' ', 2)
            return SetTopicMessage(msg[1],msg[2])
        else:
            raise Exception("Could not parse packet")