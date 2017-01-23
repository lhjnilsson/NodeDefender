from .cmdclass import *

def AddClass(classnum):
    try:
        return info, supported
    except KeyError:
        return None

def ExtendClass(classnum, supported):
    try:
        return info
    except KeyError:
        return None

def Event(**kwargs):
    try:
        return eval(kwargs['descr'] + '.Event')(**kwargs)
    except NameError:
        print(kwargs['descr'], " Not implemented")
    except KeyError:
        print("Descr not found")

    return False


def Load(*classlist):
    supported = []
    unsupported = []
    print('classlist ', classlist)
    for cmdclass in classlist:
        try:
            supported.append(eval(cmdclass.classname + '.Load')(cmdclass.classtypes))
        except NameError:
            print("Unable to load ")
            unsupported.append(cmdclass)
        except TypeError:
            print("Not translated ")

    return supported, unsupported
