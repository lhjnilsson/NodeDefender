from functools import wraps
from . import Topic

def TopicToTuple(func):
    '''
    Takes a XML from MQTT and zips it into a Dictonary following the Common
    Message Format for iCPE
    '''
    @wraps(func)
    def zipper(*args, **kwargs):
        try:
            topic = Topic()
            splitted = args[1].split('/')
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
            return func(args[0], topic, args[2])
        except IndexError:
            return func(*args)
    return zipper

class Test:
    def __init__(self):
        pass

def CommonPayload(func):
    @wraps(func)
    def wrapper(mqttsrc, topic, payload):
        p = Test()
        print(type(payload))
        for part in payload.split(' '):
            try:
                key, value = part.split('=')
                setattr(p, key, value)
            except ValueError:
                print(part)
        return func(mqttsrc, topic, p)
    return wrapper

def SensorRules(func):
    @wraps(func)
    def zipper(*args, **kwargs):
        return func(*args, **kwargs)
    return zipper
