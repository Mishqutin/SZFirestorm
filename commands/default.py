SZFUNCS = {}

class TEMP:
    def echo(args):
        return " ".join(args[1:])
    SZFUNCS["echo"] = echo
    
    def ping(args):
        return "pong"
    SZFUNCS["ping"] = ping
    
    def show(args):
        print(" ".join(args[1:]))
        return "Done"
    SZFUNCS["show"] = show
    
    def cat(args):
        f = open(args[1], "r")
        a = f.read()
        f.close()
        return a
    SZFUNCS["cat"] = cat

    def pwd(args):
        return os.getcwd()
    SZFUNCS["pwd"] = pwd
    
