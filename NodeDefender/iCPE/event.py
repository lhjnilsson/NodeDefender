from .. import celery
from . import zwave, db
from .decorators import TopicToTuple
from ..models.redis import cmdclass as CmdclassRedis

@celery.task
@TopicToTuple
def MQTT(mqttsrc, topic, payload):
    if topic.msgtype == 'cmd':
        return
    cmdclass, event = eval(topic.msgtype + '.' + topic.action)(mqttsrc, topic, payload)
    
    if event:
        CmdclassRedis.Save(topic.macaddr, topic.sensorid, topic.cmdclass,
                           **event())
    
    return True

from .msgtype import rpt, rsp, cmd, err
