from .cmdclass import *

numtoname = {'20' : 'basic', '71' : 'alarm'}

def Info(classnum):
    try:
        classname = numtoname[str(classnum)]
    except KeyError:
        print('classnum: ' + str(classnum))
        return None, None
    
    return eval(classname + '.Info')()

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
    for cmdclass in classlist:
        try:
            supported.append(eval(cmdclass.classname + '.Load')(cmdclass.classtypes))
            print('Appended: ' + cmdclass.classname)
        except NameError:
            unsupported.append(cmdclass)
        except TypeError:
            pass

    return supported, unsupported
