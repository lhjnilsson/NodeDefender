from functools import wraps

supported = {'20' : 'basic', '71' : 'alarm'}

def NumToName(classnum):
    try:
        return supported[classnum[:2]]
    except KeyError:
        raise NotImplementedError

def Supported(classname):
    '''
    Return True if the classname is Known
    '''
    try:
        return eval(classname + '.Info')()
    except NameError:
        return False

def Info(classname, classtypes = None):
    '''
    Returns Classname, flag if Class- types and Fields for Web
    '''
    try:
        if classtypes:
            return eval(classname + '.Info')(classtypes)
        else:
            return eval(classname + '.Info')()
    except NameError:
        raise NotImplementedError

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

class ClassInfo:
    classname = DataDescriptor('classname')
    classnumber = DataDescriptor('classnumber')
    types = DataDescriptor('types')
    fields = DataDescriptor('fields')
    def __init__(self):
        self.classname = None
        self.classnumber = None
        self.types = None
        self.fields = None

class BaseModel:
    sensorid = DataDescriptor('sensorid')
    instance = DataDescriptor('instance')
    vid = DataDescriptor('vid')
    ptype = DataDescriptor('ptype')
    pid = DataDescriptor('pid')
    classnumber = DataDescriptor('classnumber')
    classname = DataDescriptor('classname')
    classtype = DataDescriptor('classtype')
    subfunc = DataDescriptor('subfunc')
    enabled = DataDescriptor('enabled')

    def __init__(self):
        self.sensorid = None
        self.instance = None
        self.vid = None
        self.ptype = None
        self.pid = None
        self.classnumber = None
        self.classname = None
        self.subfunc = None
        self.classtype = None
        self.value = None
        self.enabled = False
    
    def __call__(self):
        return self._retdata

class ZWaveEvent:
    def __init__(self):
        super().__init__()

def PayloadSplitter(model=BaseModel):
    def decorate(func):
        @wraps(func)
        def wrapper(payload):
            ZWaveEvent = type('ZWaveEvent', (model, BaseModel), dict())()
            for key in dir(payload):
                if '_' in key:
                    pass
                else:
                    setattr(ZWaveEvent, key, getattr(payload, key))
            return func(ZWaveEvent)
        return wrapper
    return decorate

from . import db
from .cmdclass import alarm, basic, meter
