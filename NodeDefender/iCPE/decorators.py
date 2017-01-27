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

def PayloadToDict(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        newdict = {}
        payload = str(args[2]).split(' ')
        
        if len(payload) < 2: # String Response like "0xFF, or NodeList"
            return func(*args)

        for x in payload: # XML- based response
            y = x.split('=')
            try:
                newdict[y[0]] = y[1]
            except IndexError:
               pass
        return func(args[0], args[1], newdict)
    return wrapper

def SensorRules(func):
    @wraps(func)
    def zipper(*args, **kwargs):
        return func(*args, **kwargs)
    return zipper
