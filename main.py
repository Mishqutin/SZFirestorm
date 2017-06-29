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
os.chdir(userInfo["userLocation"])
        

s = socket.socket()
s.bind(("localhost", 8192))

myName = "main@localhost"

s.listen(1)
print("Listening started. Searching for clients...")


while True:
    c, address = s.accept()
    data = sNet.recv(c)
    
    if userInfo["outputCommands"]:
        print("Data received:")
        print(data)
    
    szAddress = data[:data.find("::")]
    szCommands = data[data.find("::")+2:].replace("\\n", "\n")
    args = szCommands.split()
    
    if not userInfo["acceptFaction"] and not szAddress == userInfo["factionTag"]+"."+userInfo["userName"]+"@"+userInfo["IP"]:
        print("Access denied for "+szAddress)
        sNet.send(c, "Access denied")
        c.close()
        continue
    elif userInfo["acceptFaction"] and not szAddress[:3] == userInfo["factionTag"]:
        print("Access denied for "+szAddress)
        sNet.send(c, "Access denied")
        c.close()
        continue
    
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
    
    c.close()
