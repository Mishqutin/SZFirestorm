# Importing
import socket
import select
import os
import time
from syztemNetwork import sNet
# ---------

#====================
#=Defining variables=
#====================

# Set necessary values.
mainDirectory = os.getcwd() # Main directory of program.

# Read config and save it to list.
f = open("SZCONFIG.szi", "r")
userInfo = eval(f.read())
f.close()

# Declare command package dictionary.
cmdList = {}


# Go to /commands in main directory.
os.chdir("commands")

for i in os.listdir():
    # Loop over all files in directory.
    if i[-3:]==".py":
        # If file has ".py" format read it and execute in global
        # so we have all it's values in global scope.
        f = open(i, "r")
        exec(f.read(), globals())
        f.close()
        
        # Our program should have set the SZFUNCS to dictionary with keys as commands' names and values as functions.
        cmdList[i[:-3]] = SZFUNCS # So we create a new key in cmdList named like package name with SZFUNCS value.
# -------------------------------------------


#====================
#=Initialize program=
#====================


# Change directory to where the 'user' type object exists.
os.chdir(userInfo["userLocation"])

# If couldn't find 'user' object at "userLocation" create new one.
if not os.path.isdir("USER."+userInfo["userName"]):
    print("Could not find user, creating new one... ", end="")
    
    os.system("mkdir USER."+userInfo["userName"])
    os.system("mkdir USER."+userInfo["userName"]+"\\backpack")
    
    info = {'divideDir': True, 'restrictAccess': True, 'name': userInfo["userName"], 'object': 'user'}
    
    f = open("USER."+userInfo["userName"]+"\\__info.szi", "w")
    f.write(str(info))
    f.close()
    print("Done")
# -------------------------------------------------------------
 


 
# Create a socket to receive data.
s = socket.socket()
s.bind(("localhost", 8192))


s.listen(1) # Listen for clients.
print("Listening started. Searching for clients...")


#===========
#=MAIN LOOP=
#===========

while True:
    # Accept and receive data from clients.
    c, address = s.accept()
    data = sNet.recv(c)
    
    
    # Print recieved data to console if it's set to True in config.
    if userInfo["outputCommands"]:
        print("Data received:")
        print(data)
    # ------------------------------------------------------------
    
    
    # Separate received data to string.
    szAddress = data[ :data.find("::") ]  # .find("::") returns beginning index of "::", so szAddress equals text before "::".
    szCommands = data[ data.find("::")+2: ].replace("\\n", "\n") # Replace text "\n" to new line.
    
    args = szCommands.split() # Split string in words to list.
    # -------------------------------
    
    
    
    
    # Check if client is permitted to send data
    if not userInfo["acceptFaction"] and not szAddress == userInfo["factionTag"]+"."+userInfo["userName"]:
        # It will execute data only from user name defined in config that begins with faction tag.
        print("Access denied for "+szAddress) # If identifier was invalid print out wich one got denied
        
        sNet.send(c, "Access denied") # and then send a message to him.
        
        c.close() # Close connection
        continue  # and go back to loop start.
        
    elif userInfo["acceptFaction"] and not szAddress[:3] == userInfo["factionTag"]:
        # If user set acceptFaction in config to True, then it will accept every data wich's identifier begins with
        # specified three-letter faction tag.
        print("Access denied for "+szAddress)
        
        sNet.send(c, "Access denied")
        
        c.close()
        continue
        # Same as above.
        # You can use it as an example to create your own veryfing system.
    # ------------------------------------------
    
    
    
    
    
    
    
    # Check if received command is a valid command.
    # cmdList = {
    # "command_Package_1" : { "commandName":function }
    # }
    notFound = 0 
    for i in cmdList: # Loop over command packages dictionary.
    
        if args[0] in cmdList[i]:
            # If first parameter (command) exists in package 'i' then execute it's function with parameters list as argument.
            reply = cmdList[i][args[0]](args) # Then save it's return value to reply.
            
            sNet.send(c, str(reply)) # And send reply as string.
            
            notFound = 0 # Set "notFound" to 0 in case it was 1.
            break # End searching.
            
        else:
            # If there wasn't any command like specified, set "notFound" to 1
            notFound = 1
    
    
    # If "notFound" is True, so command wasn't found, then send error message instead.
    if notFound: sNet.send(c, "Unsupported command: " + args[0])
    
    
    
    # Close connection.
    c.close()
