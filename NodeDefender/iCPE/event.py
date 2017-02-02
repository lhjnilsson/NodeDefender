from .. import celery
from . import zwave, db
from .decorators import TopicToTuple

@celery.task
@TopicToTuple
def MQTT(mqttsrc, topic, payload):
    if topic.msgtype == 'cmd':
        return
    cmdclass, event = eval(topic.msgtype + '.' + topic.action)(mqttsrc, topic, payload)
    
    if event:
        CmdclassRedis.Save(icpe.mac, sensor.sensorid, cmdclass.classname,
                           **event.data)
    
    return True

from .msgtype import rpt, rsp, cmd, err
