from collections import namedtuple
from functools import wraps
from .. import celery
from . import db
from .msgtype import cmd, err, rpt, rsp

topic = namedtuple("topic", "macaddr msgtype sensorid cmdclass action")

def TopicToTuple(func):
    '''
    Takes a XML from MQTT and zips it into a Dictonary following the Common
    Message Format for iCPE
    '''
    @wraps(func)
    def zipper(*args, **kwargs):
        try:
            splitted = args[1].split('/')
            return func(args[0],
                        topic(splitted[1][2:], # macaddr
                           splitted[2], # msgtype
                           splitted[4], # sensorid
                           splitted[6], # cmdclass
                           splitted[8]), # action
                        args[2])
        except IndexError:
            return func(*args)
    return zipper

def PayloadToDict(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        newdict = {}
        payload = str(args[2]).split(' ')
        for x in payload:
            y = x.split('=')
            try:
                newdict[y[0]] = y[1]
            except IndexError:
                pass
        return func(args[0], args[1], newdict)
    return wrapper

def JSONToDict(func):
    pass

def SensorRules(func):
    @wraps(func)
    def zipper(*args, **kwargs):
        return func(*args, **kwargs)
    return zipper

@celery.task
@TopicToTuple
@PayloadToDict
def MQTTEvent(mqttsrc, topic, payload):
    if topic.msgtype == 'cmd':
        return
    sensor = db.sensor.Get(topic.macaddr, topic.sensorid)
    if sensor is None:
        sensor = db.Load(mqttsrc, topic.macaddr, topic.sensorid)

    evt = eval(topic.msgtype + '.' + topic.action)(mqttsrc, topic, payload)
    
    if evt:
        return db.sensor.Save(topic.macaddr, topic.sensorid, **evt)
    else:
        return None

@celery.task
def JSON(topic, payload):
    pass
