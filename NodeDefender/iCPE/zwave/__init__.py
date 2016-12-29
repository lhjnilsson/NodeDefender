import classes

def event(commandclass, value, evttype):
    classname = HexToName(commandclass)
    if evttype:
        evetname = HexToName(evttype)
        return eval('classes.'+classname+eventname)(value)
    else:
        return eval('classes.'+classname)(value)

