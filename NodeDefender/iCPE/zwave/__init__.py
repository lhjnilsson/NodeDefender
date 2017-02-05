from functools import wraps

numtoname = {'20' : 'basic', '71' : 'alarm'}

def Supported(classname):
    try: 
        eval(classname + '.Info')()
        return True
    except NameError:
        return False

def Info(classnum):
    try:
        classname = numtoname[str(classnum)]
    except KeyError:
        print('classnum: ' + str(classnum))
        return None, None, None
    
    return eval(classname + '.Info')()

def InfoTypes(classname, classtypes):
    try:
        return eval(classname + '.InfoTypes')(classtypes)
    except KeyError:
        return None

def ExtendClass(classnum, supported):
    try:
        return info
    except KeyError:
        return None

def Event(topic, payload):
    print("TOPIC: " + topic.cmdclass)
    try:
        return eval(topic.cmdclass + '.Event')(payload)
    except NameError as e:
        print(topic.cmdclass + str(e))
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
                try:
                    key, value =  part.split('=')
                    setattr(m, key, value)
                except ValueError:
                    pass

            return func(m)
        return wrapper
    return decorate

from .cmdclass import alarm, basic
