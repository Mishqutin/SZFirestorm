import socket
import os
import time

myName = "QTN.Humvee"

docsDir = os.getcwd()

f = open("dirInfo.szi", "r")
dirInfo = eval(f.read())
f.close()

def updateDirInfo():
    f = open(docsDir+"\\dirInfo.szi", "w")
    f.write(str(dirInfo))
    f.close()

def getCommands():
    f = open("cmd.txt", "r")
    cmd = f.read()
    f.close()
    
    if cmd==" ": return False
    else: return eval(cmd)


while True:
    time.sleep(0.8)
    