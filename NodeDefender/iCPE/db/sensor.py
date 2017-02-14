from ...models.manage import sensor as SensorSQL
from ...models.redis import sensor as SensorRedis
from . import redisconn, icpe
from .. import mqtt, zwave
from ... import celery
from datetime import datetime
from .. import logger
from ..decorators import CommonPayload

@CommonPayload
def Verify(topic, payload, mqttsrc = None):
    if len(SensorRedis.Get(topic.macaddr, topic.sensorid)):
        return True
    
    if SensorRedis.Load(topic.macaddr, topic.sensorid):
        return True

    icpe.Verify(topic, payload, mqttsrc)
    Add(topic, payload)
    return mqtt.sensor.Query(topic.macaddr, topic.sensorid, **mqttsrc)

def Add(topic, payload):
    try:
        zinfo = zwave.db.SensorInfo(payload.vid, payload.pid)
    except AttributeError:
        print(payload)
        zinfo = None
    SensorSQL.Create(topic.macaddr, topic.sensorid, zinfo)
    SensorRedis.Load(topic.macaddr, topic.sensorid)
    return True
