from cmdclass import *

@ToDict
def event(event):
    classname = HexToName(commandclass)
    if evttype:
        evetname = HexToName(evttype)
        return eval(classname + '.' + eventname)(value)
    else:
        return eval(classname)(value)
