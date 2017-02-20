from .. import celery
from . import zwave, db
from .decorators import TopicToTuple
from ..models.redis import cmdclass as CmdclassRedis
from ..models.redis import field as FieldRedis
from .zwave import ZWaveEvent
from ..conn.websocket import CmdclassEvent

@celery.task
@TopicToTuple
def MQTT(topic, payload, mqttsrc):
    if topic.msgtype == 'cmd':
        return
    event = eval(topic.msgtype + '.' + topic.action)(topic, payload,
                                                              mqttsrc)
    if 'value' in dir(event):
        FieldRedis.Update(topic.macaddr, topic.sensorid, event.name,
                          event.value)
        CmdclassEvent(topic.macaddr, topic.sensorid, topic.cmdclass,
                      event.value)
    return True

@celery.task
def Socket(macaddr, sensorid, cmdclass, classtype, event):
    return True

from .msgtype import rpt, rsp, cmd, err
