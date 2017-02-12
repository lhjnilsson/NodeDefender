from functools import wraps
from . import Topic

def TopicToTuple(func):
    '''
    Takes a XML from MQTT and zips it into a Dictonary following the Common
    Message Format for iCPE
    '''
    @wraps(func)
    def zipper(oldtopic, payload, mqttsrc):
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

def CommonPayload(func):
    @wraps(func)
    def wrapper(topic, payload, mqttsrc):
        p = PayloadContainer()
        for part in payload.split(' '):
            try:
                key, value = part.split('=')
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
