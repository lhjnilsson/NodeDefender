from functools import wraps

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

def Event(topic, payload):
    print("TOPIC: " + topic.cmdclass)
    return
    try:
        return eval(topic.cmdclass + '.Event')(**kwargs)
    except NameError:
        print(topic.cmdclass, " Not implemented")
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


class DataDescriptor:
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        raise AttributeError("Can't delete me")


class BaseModel:
    sensorid = DataDescriptor('sensorid')
    instance = DataDescriptor('instance')
    vid = DataDescriptor('vid')
    ptype = DataDescriptor('ptype')
    pid = DataDescriptor('pid')
    classnumber = DataDescriptor('classnumber')
    classname = DataDescriptor('classname')
    subfunc = DataDescriptor('subfunc')

    def __init__(self):
        self.sensorid = None
        self.instance = None
        self.vid = None
        self.ptype = None
        self.pid = None
        self.classnumber = None
        self.classname = None
        self.subfunc = None
        self.data = {}

def PayloadSplitter(model=BaseModel):
    def decorate(func):
        @wraps(func)
        def wrapper(payload):
            m = model()
            for part in payload.split(' '):
                for key, value in part.split('='):
                    setattr(m, key, value)
            return func(m)
        return wrapper
    return decorate

from .cmdclass import *
