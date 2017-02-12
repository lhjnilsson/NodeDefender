from .. import celery
from . import zwave, db
from .decorators import TopicToTuple
from ..models.redis import cmdclass as CmdclassRedis

@celery.task
@TopicToTuple
def MQTT(topic, payload, mqttsrc):
    if topic.msgtype == 'cmd':
        return
    cmdclass, event = eval(topic.msgtype + '.' + topic.action)(topic, payload,
                                                              mqttsrc)
    
    if event:
        CmdclassRedis.Save(topic.macaddr, topic.sensorid, topic.cmdclass,
                           **event())
    
    return True

from .msgtype import rpt, rsp, cmd, err
