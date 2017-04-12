from .. import celery, loggHandler
from ..models.manage import icpe as iCPESQL
from ..models.manage import field as FieldSQL
from ..models.redis import field as FieldRedis
from ..models.redis import icpe as iCPERedis
from ..models.redis import sensor as SensorRedis
from ..models.redis import cmdclass as CmdclassRedis
from celery.utils.log import get_task_logger
import logging

logger = logging.getLogger('iCPE')
logger.setLevel('INFO')
logger.addHandler(loggHandler)
log = get_task_logger(__name__)
log.addHandler(loggHandler)

def Load(icpes = None):
    '''
    Loads iCPEs and Sensors
    Tries to load cmdclasses to sensor, recieved NotImplementedError from
    Redis- handler in the classname is not specific(the class is not
                                                    supported).
    if so it tries to add the class.
    '''
    if icpes is None:
        icpes = iCPESQL.List()
    
    for icpe in icpes:
        if not icpe.enabled:
            continue
        iCPERedis.Load(icpe)
        for sensor in icpe.sensors:
            SensorRedis.Load(sensor)
            for cmdclass in sensor.cmdclasses:
                try:
                    CmdclassRedis.Load(cmdclass)
                except NotImplementedError:
                    db.cmdclass.Add(icpe.macaddr, sensor.sensorid,
                                          cmdclass.classnumber)

    for field in FieldSQL.List():
        FieldRedis.Load(field)
    return True


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

from . import db, event, decorators
from .msgtype import cmd, err, rpt, rsp
