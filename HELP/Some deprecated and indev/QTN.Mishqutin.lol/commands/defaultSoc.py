SZFUNCS = {}

class TEMP:
    
    def printOut(args):
        return " ".join(args[1:])
    SZFUNCS["print"] = printOut
    
    def sleepTime(args):
        time.sleep(float(args[1]))
        return False
    SZFUNCS["sleep"] = sleepTime