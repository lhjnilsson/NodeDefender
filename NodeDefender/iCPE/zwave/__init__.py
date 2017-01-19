from .cmdclass import *

numname = {'71' : 'alarm', '20' : 'basic'}

def Classname(classnum):
    try:
        return numname[classnum]
    except KeyError:
        return None

def Event(sensor, payload):
    print("ZWave Event")
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
    print(classlist)
    return
    for cmdclass in classlist:
        try:
            supported.append(eval(cmdclass.classname + '.Load')(cmdclass.classtypes))
        except NameError:
            print("Unable to load ")
            unsupported.append(cmdclass)
        except TypeError:
            print("Not translated ")

    return supported, unsupported
