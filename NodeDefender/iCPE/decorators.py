from collections import namedtuple
from functools import wraps

topic = namedtuple("topic", "mac msgtype nodeid cmdclass action")

def TopicToTuple(func):
    '''
    Takes a XML from MQTT and zips it into a Dictonary following the Common
    Message Format for iCPE
    '''
    @wraps(func)
    def zipper(*args, **kwargs):
        try:
            splitted = args[0].split('/')
            return func(topic(splitted[1][2:], # Mac, minus the 0x
                           splitted[2], # Msgtype
                           splitted[4], # NodeID
                           splitted[6], # CommandClass
                           splitted[8]), # Action
                    args[1])
        except IndexError:
            return func(*args)
    return zipper

def JSONToDict(func):
    pass
