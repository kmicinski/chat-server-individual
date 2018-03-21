class Message:
    """Abstract base class for representing messages sent to clients"""
    def __init__(self):
        pass
    
    def render(self):
        """Expected to return bytes"""
        pass

class JoinMessage(Message):
    def __init__(self,channel,fromuser=None):
        self.fromuser = fromuser
        self.channel = channel

    def render(self):
        return "join {}".format(self.channel)

class UpdatePasswordMessage(Message):
    def __init__(self,newpassword):
        self.newpassword = newpassword

    def render(self):
        "updatepassword {}".format(self.newpassword)

class BlockMessage(Message):
    def __init__(self,user):
        self.blockeduser = user

    def render(self):
        "block {}".format(self.blockeduser)

class BanMessage(Message):
    def __init__(self,user,channel):
        self.banneduser = user
        self.channel = channel

    def render(self):
        "ban {} {}".format(self.banneduser,self.channel)

class UnbanMessage(Message):
    def __init__(self,user,channel):
        self.banneduser = user
        self.channel = channel

    def render(self):
        "unban {} {}".format(self.banneduser,self.channel)

class GetTopicMessage(Message):
    def __init__(self,channel):
        self.channel = channel

    def render(self):
        return "gettopic {}".format(self.channel)

class SetTopicMessage(Message):
    def __init__(self,channel,topic):
        self.channel = channel
        self.topic = topic

    def render(self):
        return "settopic {} {}".format(self.channel,self.topic)

class TopicMessage(Message):
    def __init__(self,channel,topic):
        self.channel = channel
        self.topic = topic 

    def render(self):
        return "topic {} {}".format(self.channel,self.topic)

    def __eq__(self,other):
        return self.channel == other.channel and self.topic == other.topic

    def __ne__(self,other): 
        return not self.__eq__(other)

class AuthenticateMessage(Message):
    def __init__(self,username,password):
        self.username = username
        self.password = password

    def render(self):
        "authenticate {} {}".format(username, password)

class RegisterMessage(Message):
    def __init__(self,username,password):
        self.username = username
        self.password = password

    def render(self):
        "register {} {}".format(username, password)

class ChatMessage(Message):
    def __init__(self,user_or_channel,message):
        self.user_or_channel = user_or_channel
        self.message = message
    
    def render(self):
        m = "chat {} {} {}".format(self.user_or_channel,len(self.message),self.message)
        return m.encode()

class ChatFromMessage(Message):
    """A reply from the server notifying a client that they have received a message from either a user or a channel"""
    def __init__(self,fromuser,channel,message):
        self.fromuser = fromuser
        self.channel = message
        self.message = message
    
    def render(self):
        m = "chatfrom {} {} {}".format(self.fromuser,self.channel,self.message)
        return m.encode()

class ErrorMessage(Message):
    """Indicates that some errror has occurred"""
    def __init__(self,message):
        self.message = message
    
    def render(self):
        m = "error {} {}".format(len(self.message), self.message)
        return m.encode()
