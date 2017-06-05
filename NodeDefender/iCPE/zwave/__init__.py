from functools import wraps

supported = {'20' : 'basic', '25' : 'bswitch', '32' : 'meter', '71' : 'alarm'}

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
        return eval('commandclass.' + classname + '.Info')()
    except NameError:
        return False

def Info(classnumber, classtypes = None):
    '''
    Returns Classname, flag if Class- types and Fields for Web
    '''
    if classnumber not in supported:
        return False

    classname = supported[classnumber]
    try:
        if classtypes:
            return eval('commandclass.' + classname + '.Info')(classtypes)
        else:
            return eval('commandclass.' + classname + '.Info')()
    except AttributeError:
        raise NotImplementedError

def Event(topic, payload):
    '''
    Z-Wave event. Tries to lookup if the event is known(supported) or not
    '''
    try:
        return eval('commandclass.' + topic.commandclass + '.Event')(payload)
    except AttributeError as e:
        print(topic.commandclass + str(e))
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

    subfunc = DataDescriptor('subfunc')
    value = DataDescriptor('value')
    field = DataDescriptor('field') 

    cc = DataDescriptor('cc')
    ccname = DataDescriptor('ccname')
    cctype = DataDescriptor('cctype')
    cctypename = DataDescriptor('cctypename')
    ccevent = DataDescriptor('ccevent')

    icon = DataDescriptor('icon')
    state = DataDescriptor('state')

    def __init__(self):
        self.sensorid = None
        self.instance = None
        self.vid = None
        self.ptype = None
        self.pid = None
        self.subfunc = None
        self.value = None
        self.field = None
        self.cc = None
        self.ccname = None
        self.cctype = None
        self.cctypename = None
        self.ccevent = None

        self.icon = None
        self.state = None

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
                    continue
                if key == 'class':
                    setattr(ZWaveEvent, 'cls', getattr(payload, key))
                else:
                    setattr(ZWaveEvent, key, getattr(payload, key))
            return func(ZWaveEvent)
        return wrapper
    return decorate

from . import db, commandclass
