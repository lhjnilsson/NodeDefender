from .cmdclass import *

def Event(event):
    classname = HexToName(commandclass)
    if evttype:
        evetname = HexToName(evttype)
        return eval(classname + '.' + eventname)(value)
    else:
        return eval(classname)(value)

def Load(*classlist):
    supported = []
    unsupported = []
    for cmdclass in classlist:
        cmdname = ClassToName(cmdclass)
        if cmdname:
            try:
                supported.append(eval(cmdclass + '.Load')())
            except NameError:
                print("Unable to load ", cmdname)
        else:
            unsupported.append(cmdclass)

    return supported, unsupported
