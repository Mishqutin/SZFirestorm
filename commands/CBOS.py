SZFUNCS = {}

def findObjByName(name, path="."):
    for i in os.listdir(path):
        if os.path.isfile(i+"/__info.szi"):
            f = open(i+"/__info.szi", "r")
            info = eval(f.read())
            f.close()
            if info["name"] == name:
                return i
                break
    return False

class TEMP:
    
    def ls(args):
        string = ""
        objects = []
        files = []
        
        for i in os.listdir():
            if os.path.isdir(i) and os.path.isfile(i+"/__info.szi"):
                f = open(i+"/__info.szi", "r")
                data = f.read()
                info = eval(data)
                f.close()
                
                if info["divideDir"]: objects.append(info["name"])
                
            else: files.append(i)
        
        string = "===Directories and files found:\n"
        for i in files: string += i+"\n"
        
        string += "===Syztem objects found:\n"
        for i in objects: string +=i+"\n"
        
        string += "==="
        return string
    SZFUNCS["ls"] = ls
    
    def cd(args):
        dir = " ".join(args[1:])
        if os.path.isdir(dir):
            if os.path.isfile(dir+"/__info.szi"):
                f = open(dir+"/__info.szi", "r")
                info = eval(f.read())
                f.close
                if info["restrictAccess"]: return "Unable to complete. Access restricted: "+dir
            os.chdir(dir)
            return "Done"
        else: return "Directory does not exist."
    SZFUNCS["cd"] = cd
    
    
    def use(args):
        try: obj = findObjByName(args[1])
        except: return "Missing data."
        if not obj: return "Object doesn't exist."
        if not os.path.isfile(obj+"/main.py"): return "Missing main file in object's directory!"
        f = open(obj+"/main.py", "r")
        code = f.read()
        f.close()
        exec(code, globals())
        return SZReturnValue
    SZFUNCS["use"] = use
    
    def obj_create(args):
        info = {"object":"SZO", "divideDir":True, "restrictAccess":True, "name":args[1]}
        
        # Getting last stamp code
        f = open(mainDirectory + "/SZSTAMP.txt", "r")
        lastStamp = f.read()
        f.close()
        # Updating last stamp code file
        f = open(mainDirectory + "/SZSTAMP.txt", "w")
        f.write( str(eval(lastStamp)+1) )
        f.close()
        
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
        
        
