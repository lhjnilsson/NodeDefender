from collections import namedtuple
from functools import wraps

topic = namedtuple("topic", "mac type sensor class action")

def TopicToTuple(func):
    '''
    Takes a XML from MQTT and zips it into a Dictonary following the Common
    Message Format for iCPE
    '''
    @wraps(func)
    def zipper(*args, **kwargs):
        try:
            splitted = args[0].split('/')
            return func(topic(splitted[1][2:], # mac
                           splitted[2], # type
                           splitted[4], # sensor
                           splitted[6], # class
                           splitted[8]), # action
                    args[1])
        except IndexError:
            return func(*args)
    return zipper

def JSONToDict(func):
    pass
