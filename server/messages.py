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
        m = "join {}".format(self.channel)
        return m.encode()

class UpdatePasswordMessage(Message):
    def __init__(self,newpassword):
        self.newpassword = newpassword

    def render(self):
        m = "update_pw {}".format(self.newpassword)
        return m.encode()

class BlockMessage(Message):
    def __init__(self,user):
        self.blockeduser = user

    def render(self):
        m = "block {}".format(self.blockeduser)
        return m.encode()

class BanMessage(Message):
    def __init__(self,user,channel):
        self.banneduser = user
        self.channel = channel

    def render(self):
        m = "ban {} {}".format(self.banneduser,self.channel)
        return m.encode()

class UnbanMessage(Message):
    def __init__(self,user,channel):
        self.banneduser = user
        self.channel = channel

    def render(self):
        m = "unban {} {}".format(self.banneduser,self.channel)
        return m.encode()

class GetTopicMessage(Message):
    def __init__(self,channel):
        self.channel = channel

    def render(self):
        m = "gettopic {}".format(self.channel)
        return m.encode()

class SetTopicMessage(Message):
    def __init__(self,channel,topic):
        self.channel = channel
        self.topic = topic

    def render(self):
        m = "settopic {} {}".format(self.channel,self.topic)
        return m.encode()

class TopicMessage(Message):
    def __init__(self,channel,topic):
        self.channel = channel
        self.topic = topic 

    def render(self):
        m = "topic {} {}".format(self.channel,self.topic)
        return m.encode()
    
class AuthenticateMessage(Message):
    def __init__(self,username,password):
        self.username = username
        self.password = password

    def render(self):
        m = "authenticate {} {}".format(username, password)
        return m.encode()

class RegisterMessage(Message):
    def __init__(self,username,password):
        self.username = username
        self.password = password

    def render(self):
        m = "register {} {}".format(username, password)
        return m.encode()

class ChatMessage(Message):
    def __init__(self,user_or_channel,message):
        self.user_or_channel = user_or_channel
        self.message = message
    
    def render(self):
        m = "chat {} {}".format(self.user_or_channel,self.message)
        return m.encode()

class ChatFromMessage(Message):
    """A reply from the server notifying a client that they have received a message from either a user or a channel"""
    def __init__(self,fromuser,channel,message):
        self.fromuser = fromuser
        self.channel = channel
        self.message = message
    
    def render(self):
        m = "chatfrom {} {} {}".format(self.fromuser,self.channel,self.message)
        return m.encode()

class ErrorMessage(Message):
    """Indicates that some errror has occurred"""
    def __init__(self,message):
        self.message = message
    
    def render(self):
        m = "error {}".format(self.message)
        return m.encode()
