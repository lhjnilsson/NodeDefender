from .. import celery
from . import zwave, db
from .decorators import TopicToTuple

ZWave = celery.task(zwave.Event)

@celery.task
@TopicToTuple
def MQTT(mqttsrc, topic, payload):
    if topic.msgtype == 'cmd':
        return
    icpe, sensor, cmdclass, zwave  = eval(topic.msgtype + '.' + topic.action)(mqttsrc, topic, payload)
    
    if zwave:
        zwave.get()

    if cmdclass:
        CmdclassRedis.Save(icpe.mac, sensor.sensorid, cmdclass.classname,
                           **zwave.data)
    return True

from .msgtype import rpt, rsp, cmd, err
