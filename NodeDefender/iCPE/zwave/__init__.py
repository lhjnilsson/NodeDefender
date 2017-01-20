from .cmdclass import *

def Classname(classnum):
    try:
        return numname[classnum]
    except KeyError:
        return None

def Event(**kwargs):
    try:
        return eval(kwargs['descr'] + '.Event')(**kwargs)
    except NameError:
        print(kwargs['descr'], " Not implemented")
    except KeyError:
        print("Descr not found")


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
