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
    return True

def Add(topic, payload):
    zinfo = zwave.db.SensorInfo(payload.vid, payload.pid)
    SensorSQL.Create(topic.macaddr, topic.sensorid, zinfo)
    SensorRedis.Load(topic.macaddr, topic.sensorid)
    return True
