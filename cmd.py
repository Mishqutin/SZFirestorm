import socket
import time
from syztemNetwork import sNet

myName = "Mishqutin@localhost"

s = socket.socket()
s.connect(("localhost", 8192))

sNet.send(s, myName)
name = sNet.recv(s)
if not name=="main@localhost":
    print("Not that host: "+name)
    exit()

while True:
    x = input("$ ")
    sNet.send(s, x)
    print(sNet.recv(s).replace("\\n", "\n"))
    if x=="disconnect" or x=="close":
        s.close()
        break
