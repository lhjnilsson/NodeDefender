from functools import wraps

numtoname = {'20' : 'basic', '71' : 'alarm'}

def Supported(classname):
    '''
    Return True if the classname is Known
    '''
    try: 
        eval(classname + '.Info')()
        return True
    except NameError:
        return False

def Info(classnum):
    '''
    Returns Classname, flag if Class- types and Fields for Web
    '''
    try:
        classname = numtoname[str(classnum)]
    except KeyError:
        return None, None, None
    
    return eval(classname + '.Info')()

def InfoTypes(classname, classtypes):
    '''
    Returns information about Classtypes
    '''
    try:
        return eval(classname + '.InfoTypes')(classtypes)
    except KeyError:
        return None

def Event(topic, payload):
    '''
    Z-Wave event. Tries to lookup if the event is known(supported) or not
    '''
    try:
        return eval(topic.cmdclass + '.Event')(payload)
    except NameError as e:
        print(topic.cmdclass + str(e))
    except KeyError:
        print("Descr not found")

    return False


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
        self._retdata = {}
    
    def __call__(self):
        return self._retdata

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

from .cmdclass import alarm, basic, meter
