from user import *
from messages import *

class State:
    """"Class for managing the global state of the server"""
    def __init__(self):
        self.users = {} # No current users
        self.channels = {} # No current channels
        self.loggedin_usernames = []
        self.connections = {} # Map from usernames to Connection objects

    def register(self,username,password):
        """Register a new user with a specified username and password."""
        # Can't add a user to the set of users that's already there..
        if username not in self.users:
            u = User(username,password,[])
            self.users[username] = u
            self.loggedin_usernames.append(username)
            return u
        else:
            raise Exception("Error: trying to register an account that already exists")

    def register_observer(self,username,connection):
        """Add a connection object to the list of observers"""
        self.connections[username] = connection

    def authenticate(self,username,password):
        """Log in a user that's already registered"""
        if username not in self.loggedin_usernames:
            if username in users:
                u = self.users[username]
                if (password == u.password):
                    # Log in the user
                    self.loggedin_usernames.insert(username)
                    return u
                else:
                    raise Exception("Password incorrect")
            else:
                raise Exception("No such user is currently registered")
        else:
            raise Exception("User is already logged in")

    def notify(self,username,msg):
        """Notify the user of a certain message"""
        self.connections[username].notify(msg)

    def handle_chat(self,fromuser,to,message):
        """Perform the work to notify each user associated with a given channel or private message"""
        if to.startswith("#"):
            # To a channel
            if to in self.channels:
                chan = self.channels[to]
                for user in chan.members:
                    # Send the message to each member of this channel
                    msg = ChatFromMessage(fromuser,to,message)
                    self.notify(user.username,msg.render())
            else:
                msg = ErrorMessage("No such channel exists")
                self.notify(fromuser,msg.render())
        else:
            # To another user
            # Make sure user is logged in
            if to in self.loggedin_usernames:
                msg = ChatFromMessage(fromuser,to,message)
                notify(user,msg.render())
            else:
                msg = ErrorMessage("Target user is not logged in / does not exist")
                notify(user,msg.render())
