from collections import namedtuple
from functools import wraps

topic = namedtuple("topic", "macaddr msgtype sensorid cmdclass action")

def TopicToTuple(func):
    '''
    Takes a XML from MQTT and zips it into a Dictonary following the Common
    Message Format for iCPE
    '''
    @wraps(func)
    def zipper(*args, **kwargs):
        try:
            splitted = args[0].split('/')
            return func(topic(splitted[1][2:], # macaddr
                           splitted[2], # msgtype
                           splitted[4], # sensorid
                           splitted[6], # cmdclass
                           splitted[8]), # action
                    args[1])
        except IndexError:
            return func(*args)
    return zipper

def JSONToDict(func):
    pass

def SensorRules(func):
    @wraps(func)
    def zipper(*args, **kwargs):
        return func(*args, **kwargs)
    return zipper
