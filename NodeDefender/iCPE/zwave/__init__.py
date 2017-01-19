from .cmdclass import *

def Event(sensor, payload):
    return True
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
        try:
            supported.append(eval(cmdclass + '.Load')(cmdclass.classtypes))
        except NameError:
            print("Unable to load ", cmdname)
            unsupported.append(cmdclass)

    return supported, unsupported
