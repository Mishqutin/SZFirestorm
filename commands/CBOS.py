SZFUNCS = {}
DATA = {}

def findObjByName(name, path="."):
    if os.path.isdir(name+"\\__info.szi"):
        return name
    for i in os.listdir(path):
        if os.path.isfile(i+"\\__info.szi"):
            f = open(i+"\\__info.szi", "r")
            info = eval(f.read())
            f.close()
            if info["name"] == name:
                return i
                break
    return False

def listObjNames(path="."):
    objects = []
    files = []
    users = []
    
    for i in os.listdir(path):
        if os.path.isdir(path+"\\"+i) and os.path.isfile(path+"\\"+i+"\\__info.szi"):
            f = open(path+"\\"+i+"\\__info.szi", "r")
            data = f.read()
            info = eval(data)
            f.close()
            
            if info["object"]=="user": users.append(info["name"])
            elif info["divideDir"]: objects.append(info["name"])
        
        elif i[-4:]==".szi": continue
            
        else: files.append(i)
        
    return (files, objects, users)

def getObjInfoFile(obj, path="."):
    f = open(path+"\\"+obj+"\\__info.szi", "r")
    info = eval(f.read())
    f.close()
    return info

def getSzStamp():
        # Getting last stamp code
        f = open(mainDirectory + "/SZSTAMP.txt", "r")
        lastStamp = f.read()
        f.close()
        # Updating last stamp code file
        f = open(mainDirectory + "/SZSTAMP.txt", "w")
        f.write( str(eval(lastStamp)+1) )
        f.close()
        
        return lastStamp

class TEMP:
    
    def ls(args):
    
        files, objects, users = listObjNames()
        
        string = "===Directories and files found:\n"
        for i in files: string += i+"\n"
        
        if objects!=[]:
            string += "===Syztem objects found:\n"
            for i in objects: string +=i+"\n"
        
        if users!=[]:
            string += "===Other users found:\n"
            for i in users:
                if i == userInfo["userName"]: continue
                string += i+"\n"
        
        string += "==="
        return string
    SZFUNCS["ls"] = ls
    
    def cd(args):
        dir = " ".join(args[1:])
        currentDir = os.getcwd()
        
        if os.path.isdir(dir):
            if os.path.isfile(dir+"/__info.szi"):
                f = open(dir+"/__info.szi", "r")
                info = eval(f.read())
                f.close
                
                if info["restrictAccess"]: return "Unable to complete. Access restricted: "+dir
                
            os.chdir(dir)
            os.system("move {}\\USER.{} >> nul".format(currentDir, userInfo["userName"]))
            
            userInfo["userLocation"] = os.getcwd()
            f = open(mainDirectory+"\\SZCONFIG.szi", "w")
            f.write(str(userInfo))
            f.close()
            
            return "You are now in: "+dir
            
        else: return "Directory does not exist."
    SZFUNCS["cd"] = cd
    
    
    
    
    # Executes main.py of an item (i.e. uses item)
    def use(args):
        try: obj = findObjByName(args[1])
        except: return "Missing data."
        
        if not obj: return "Object doesn't exist."
        if not os.path.isfile(obj+"/main.py"): return "Missing main file in object's directory!"
        
        # Verify if object is an item type
        f = open(obj+"/__info.szi", "r")
        info = eval(f.read())
        f.close()
        if not info["object"]=="item": return "You can't use type " +info["object"]+ " objects!"
        
        # Execute code
        f = open(obj+"/main.py", "r")
        code = f.read()
        f.close()
        exec(code, globals())
        return SZReturnValue
    SZFUNCS["use"] = use
    
    
    
    
    # Creates new object template
    def obj_create(args):
        lastStamp = getSzStamp()
        
        try: info = {"object":args[2], "divideDir":True, "restrictAccess":True, "name":args[1]+lastStamp}
        except: return "Missing data."
        
        
        # Creating new directory
        directoryName = "{}.{}.{}".format(userInfo["factionTag"], userInfo["userName"], lastStamp)
        os.system("mkdir " + directoryName)
        
        # Creating __info.szi
        f = open(os.getcwd() + "/" +directoryName + "/__info.szi", "w")
        f.write(str(info))
        f.close()
        
        # Creating main.py
        f = open(os.getcwd() + "/" +directoryName + "/main.py", "w")
        f.write("SZReturnValue = 'Hello! I am a new object here!'")
        f.close()
        
        return "Object successfully created :)"
    SZFUNCS["obj-create"] = obj_create
    
    # Copies unit from \objects in main directory with a new id and name
    def obj_spawn_existing(args):
        name = args[1]
        
        lastStamp = getSzStamp()
        
        obj = "{}.{}.{}".format(userInfo["factionTag"], userInfo["userName"], lastStamp)
        
        os.system("mkdir "+obj)
        os.system("copy {}\\objects\\{} {}".format(mainDirectory, name, obj))
        
        info = getObjInfoFile(obj)
        info["name"] = info["name"] + lastStamp
        
        f = open(obj+"\\__info.szi", "w")
        f.write(str(info))
        f.close()
        
        
        return "Created "+name+" in "+obj
    SZFUNCS["obj-spawn"] = obj_spawn_existing
    
    # Initializes unit. Creates it's directory in Documents\Syztem\TEMP and runs it from here.
    def obj_unit_initialize(args):
        obj = findObjByName(args[1])
        if not obj: return "Cannot find unit."
        
        docsDir = "{}\\Documents\\Syztem\\TEMP\\{}".format(os.getenv("USERPROFILE"), obj)
        
        if os.path.isdir(docsDir): os.system("del /Q "+docsDir) # If unit was initialized earlier - delete dir and update it
        os.system("mkdir "+docsDir)
        os.system("copy {} {}".format(obj+"\\main.py", docsDir))
        os.system("start /D {} {}".format(docsDir, docsDir+"\\main.py"))

        # Place for compiler soc
        
        #os.system("start /D {} {} {}".format(docsDir, mainDirectory+"\\socCompiler.py", docsDir+"\\main.soc"))
        # ----
        
        dirInfo = {"mainDir":os.getcwd()+"\\"+obj}
        #
        f = open(docsDir+"\\dirInfo.szi", "w")
        f.write(str(dirInfo))
        f.close()
        
        return "Unit "+args[1]+" initialized"
    SZFUNCS["obj-init"] = obj_unit_initialize
    
    
    
    
    # Selects unit
    def obj_unit_select(args):
        obj = findObjByName(args[1])
        
        if not obj: return "Object doesn't exist."
        if not os.path.isdir("{}\\Documents\\Syztem\\TEMP\\{}".format(os.getenv("USERPROFILE"), obj)): return "Object not initialized"
        
        DATA["selected"] = obj
        return "Selected unit: "+args[1]
    SZFUNCS["select"] = obj_unit_select
    
    
    
    # Sends command to selected unit
    def obj_unit_sendCommand(args):
        obj = DATA["selected"]
        if not os.path.isdir(obj): return "Could not find unit."
        
        f = open(obj+"\\cmd.txt", "w")
        f.write(str(args[1:]))
        f.close()
        
        return "Command sent"
    SZFUNCS["-"] = obj_unit_sendCommand
    
    
    
    
    
    
    def user_backpack(args):
        if args[1]=="list":
            files, objects, users = listObjNames(".\\USER.{}\\backpack".format(userInfo["userName"]))
            
            string = "===Items stored in your backpack:\n"
            for i in objects: string +=i+"\n"
            
            string += "==="
            return string
        elif args[1]=="put":
            file = args[2]
            obj = findObjByName(file)
            
            if not obj: return "Could not find " + file
            
            os.system("move {} USER.{}\\backpack".format(obj, userInfo["userName"]))
            
            return "Item put"
        elif args[1]=="drop":
            os.chdir("USER.{}\\backpack".format(userInfo["userName"]))
            obj = findObjByName(args[2])
            os.chdir("..\\..")
            
            if not obj: return "You don't have that object in your backpack"
            os.system("move USER.{}\\backpack\\{}".format(userInfo["userName"], obj))
            return "Item dropped"
    SZFUNCS["bp"] = user_backpack
            