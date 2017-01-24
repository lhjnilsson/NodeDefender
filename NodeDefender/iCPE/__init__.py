from collections import namedtuple
from functools import wraps
from .. import celery
from ..models.manage import icpe as iCPESQL
from celery.utils.log import get_task_logger

topic = namedtuple("topic", "macaddr msgtype sensorid cmdclass action")

logger = get_task_logger(__name__)

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
    
    if type(evt) is dict:
        logger.info("Updating info for: {}:{}. Event: {}".\
                    format(topic.macaddr, topic.sensorid, evt))
        return db.sensor.Save(topic.macaddr, topic.sensorid, **evt)
    else:
        return None

def Load():
    icpes = iCPESQL.List()
    for icpe in icpes:
        db.icpe.LoadFromObject(icpe)
        logger.info("Loading iCPE {}".format(icpe.mac))
        for sensor in icpe.sensors:
            db.sensor.LoadFromObject(sensor)
            logger.info("Loading Sensor {}:{}".format(icpe.mac,
                                                      sensor.sensorid))
    return True

from . import db
from .msgtype import cmd, err, rpt, rsp
