

def Event(event):
    classname = HexToName(commandclass)
    if evttype:
        evetname = HexToName(evttype)
        return eval(classname + '.' + eventname)(value)
    else:
        return eval(classname)(value)

def Load(*classlist):
    return [], [cls for cls in classlist]
