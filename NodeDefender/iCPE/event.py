from .. import celery
from . import zwave, db, mqtt
from .decorators import TopicToTuple
from ..models.redis import cmdclass as CmdclassRedis
from ..models.redis import field as FieldRedis
from .zwave import ZWaveEvent
from ..conn.websocket import FieldEvent
from ..models.manage.data import sensor as SQLData

@celery.task
def WebSocket(macaddr, sensorid, cmdclass, value):
    mqtt.zwave.Set(macaddr, sensorid, cmdclass, value)
    return True

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
        FieldEvent(topic.macaddr, topic.sensorid, event.name,
                      event.value)
        if event.classtype == 'power' or event.classtype == 'heat':
            eval('SQLData.' + event.classtype + '.Put')(topic.macaddr, topic.sensorid,
                                         event.value)
        else:
            SQLData.event.Put(topic.macaddr, topic.sensorid, event.classname,
                          event.classtype, event.value)

    return True

@celery.task
def Socket(macaddr, sensorid, cmdclass, classtype, event):
    return True

from .msgtype import rpt, rsp, cmd, err
