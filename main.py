import socket
import select
import os
import time
from syztemNetwork import sNet

mainDirectory = os.getcwd()

f = open("SZCONFIG.szi", "r")
userInfo = eval(f.read())
f.close()

cmdList = {}

os.chdir("commands")
for i in os.listdir():
    if i[-3:]==".py":
        f = open(i, "r")
        exec(f.read(), globals())
        f.close()
        cmdList[i[:-3]] = SZFUNCS
os.chdir("../filesystem")
        

s = socket.socket()
s.bind(("localhost", 8192))

myName = "main@localhost"

s.listen(1)
print("Listening started. Searching for commmand server...")
while True:
    c, address = s.accept()
    name = sNet.recv(c)
    if not name==userInfo["userName"]+"@"+userInfo["IP"]:
        print(name)
        c.close()
    else:
        print("Found "+name)
        sNet.send(c, myName)
        break
while True:
    isData = select.select([c], [], [], 1)
    if isData[0]:
        data = sNet.recv(c)
        print("Command received:")
        print(data)
        args = data.split()
        
        notFound = 0
        for i in cmdList:
            if args[0] in cmdList[i]:
                reply = cmdList[i][args[0]](args)
                sNet.send(c, str(reply))
                notFound = 0
                break
            else:
                notFound = 1
        if notFound: sNet.send(c, "Unsupported command: " + args[0])
