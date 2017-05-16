from ...models.manage import sensor as SensorSQL
from ...models.redis import sensor as SensorRedis
from . import redisconn, cmdclass
from .. import mqtt, zwave
from ... import celery
from datetime import datetime
from .. import logger
from ..decorators import ParsePayload

@ParsePayload
def Verify(topic, payload, mqttsrc = None):
    if len(SensorRedis.Get(topic.macaddr, topic.sensorid)):
        return True
    
    if SensorRedis.Load(topic.macaddr, topic.sensorid):
        return True

    Add(topic, payload)
    return True

def Add(topic, payload):
    zinfo = zwave.db.SensorInfo(payload.vid, payload.pid)
    SensorSQL.Create(topic.macaddr, topic.sensorid, zinfo)
    SensorRedis.Load(topic.macaddr, topic.sensorid)
    return True

def Update(macaddr, sensorid):
    sensor = SensorSQL.Get(macaddr, sensorid)
    if not sensor.cmdclasses:
        mqtt.sensor.Query(macaddr, sensorid)
        return True
    for cls in sensor.cmdclasses:
        cmdclass.Update(cls)
    return True
