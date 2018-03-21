import os
import socket
import atexit
import signal
import subprocess
from time import sleep
from parser import *
from subprocess import Popen

address = "localhost"
port = 4000
SIZE = 1024
pid = None

def rest():
    sleep(.2)

def start_server():
    with open("outfile", "w") as outfile:
        with open("errfile","w") as errfile:
            pid = subprocess.Popen("python server.py example_passwords.csv".split(),stderr=errfile,stdout=outfile)
            return pid

def copy_pwds(): 
    os.system("cp example_passwords.csv thepasswords.csv")

def cleanup():
    pid.kill()
    os.system("rm thepasswords.csv 2>err")
    os.system("rm out err 2>err")

def register(socket,uname,password):
    socket.send("register {} {}".format(uname,password))
    rest()

p = Parser()

def expect(s,m1):
    d = s.recv(SIZE)
    m2 = p.parse_packet(d)
    assert m1 == m2

copy_pwds()
pid = start_server()
atexit.register(cleanup)
rest()
sock = socket.socket()
sock.connect((address, port))
if sock == None:
    raise "Could not connect to server!"
register(sock,"kristest","kristestpwd")
sock.send(JoinMessage("#foo").render())
sock.send(SetTopicMessage("#foo", "here is the example topic").render())
sock.send(GetTopicMessage("#foo").render())
expect(sock,TopicMessage("#foo", "here is the example topic"))
