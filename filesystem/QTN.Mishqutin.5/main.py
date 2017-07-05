import socket
import os
import time

myName = "QTN.relayStation"

f = open("dirInfo.szi", "r")
dirInfo = eval(f.read())
f.close()

while True:
    time.sleep(0.8)
    f = open(dirInfo["mainDir"]+"\\cmd.txt", "r")
    cmd = f.read()
    f.close
    if cmd==" ": continue
    text = " ".join(eval(cmd))
    f = open(dirInfo["mainDir"]+"\\cmd.txt", "w")
    f.write(" ")
    f.close()
    
    toSend = myName+"::"+text
    
    s = socket.socket()
    s.connect(("localhost", 8192))
    s.send(toSend.encode())
    print(str(s.recv(4096)))
    s.close()