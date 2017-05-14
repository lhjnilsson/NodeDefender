from functools import wraps

class TopicDescriptor:
    '''
    Metaclass to store MQTT Topic
    '''
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

class Topic:
    '''
    Stores the data from topic
    '''
    macaddr = TopicDescriptor("macaddr")
    msgtype = TopicDescriptor("msgtype")
    sensorid = TopicDescriptor("sensorid")
    endpoint = TopicDescriptor("endpoint")
    cmdclass = TopicDescriptor("cmdclass")
    subfunc = TopicDescriptor("subfunc")
    action = TopicDescriptor("action")
    def __init__(self):
        self.macaddr = None
        self.msgtype = None
        self.sensorid = None
        self.endpoint = None
        self.cmdclass = None
        self.subfunc = None
        self.action = None


def ParseTopic(func):
    '''
    Takes a XML from MQTT and zips it into a Dictonary following the Common
    Message Format for iCPE
    '''
    @wraps(func)
    def zipper(oldtopic, payload, mqttsrc = None):
        try:
            topic = Topic()
            splitted = oldtopic.split('/')
            topic.macaddr = splitted[1][2:]
            topic.msgtype = splitted[2]
            topic.sensorid = splitted[4].split(":")[0]
            try:
                topic.endpoint = splitted[4].split(":")[1]
            except IndexError:
                topic.endpoint = None
            topic.cmdclass = splitted[6].split(":")[0]
            try:
                topic.subfunc = splitted[6].split(":")[1]
            except IndexError:
                topic.subfunc = None
            topic.action = splitted[8]
            return func(topic, payload, mqttsrc)
        except IndexError:
            return func(oldtopic, payload, mqttsrc)
    return zipper

class PayloadContainer:
    def __init__(self):
        pass

def ParsePayload(func):
    @wraps(func)
    def wrapper(topic, payload, mqttsrc = None):
        if type(payload) is PayloadContainer:
            return func(topic, payload, mqttsrc)

        p = PayloadContainer()
        if type(payload) is PayloadContainer:
            return func(topic, payload, mqttsrc)
        for part in payload.split(' '):
            try:
                key, value = part.split('=')
                if key == 'class':
                    key = 'cls'
                    value = value[-2:]
                setattr(p, key, value)
            except ValueError:
                pass

        return func(topic, p, mqttsrc)
    return wrapper

def SensorRules(func):
    @wraps(func)
    def zipper(*args, **kwargs):
        return func(*args, **kwargs)
    return zipper
