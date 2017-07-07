# This is an experimental compiler for .soc files.
# It's unused for some time because of some problems.
# I will later try to implement it but until now Python will be used to code all objects


import os
import sys
import time

def execute(args):
    for ii in cmdList:
        if args[0] in cmdList[ii]:
            funcRet = cmdList[ii][args[0]](args)
            if funcRet != None and funcRet: print(str(funcRet))

cmdList = {}

f = open("dirInfo.szi", "r")
dirInfo = eval(f.read())
f.close()

# Same as in main.py
for i in os.listdir(dirInfo["mainDir"]+"\\commands"):
    if i[-3:]==".py":
        f = open(dirInfo["mainDir"]+"\\commands"+"\\"+i, "r")
        exec(f.read(), globals())
        f.close()
        
        cmdList[i[:-3]] = SZFUNCS
    


f = open(sys.argv[1], "r")
code = f.readlines()
f.close()


# Execution

for i in code:

    args = i.split()
    print(args)
    if args[0] == "if":
        if eval(args[1]): execute(args[2:])
    else: execute(args)


print("Program end.")
a = input()
exit()
