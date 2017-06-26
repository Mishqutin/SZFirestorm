SZFUNCS = {}

class TEMP:
    def echo(args):
        return " ".join(args[1:])
    SZFUNCS["echo"] = echo
    
    def ping(args):
        return "pong"
    SZFUNCS["ping"] = ping
    

    

