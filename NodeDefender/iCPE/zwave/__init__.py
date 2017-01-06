from cmdclass import *

@ToDict
def Event(event):
    classname = HexToName(commandclass)
    if evttype:
        evetname = HexToName(evttype)
        return eval(classname + '.' + eventname)(value)
    else:
        return eval(classname)(value)

def Load(cmdclass, classtypes):
    return {'NO' : True}
