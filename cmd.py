import socket
import time
from syztemNetwork import sNet

myName = "QTN.Mishqutin@localhost"



while True:
    x = input("$ ")
    s = socket.socket()
    s.connect(("localhost", 8192))
    sNet.send(s, myName+"::"+x)
    print(sNet.recv(s).replace("\\n", "\n"))
    s.close()
