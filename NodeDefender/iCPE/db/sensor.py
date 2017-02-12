from ...models.manage import sensor as SensorSQL
from ...models.redis import sensor as SensorRedis
from . import redisconn, icpe
from .. import mqtt, zwave
from ... import celery
from datetime import datetime
from .. import logger

def Verify(topic, payload, mqttsrc):
    if len(SensorRedis.Get(topic.macaddr, topic.sensorid)):
        return SensorRedis.Get(topic.macaddr, topic.sensorid)
    else:
        if SensorSQL.Get(topic.macaddr, topic.sensorid):
            return SensorRedis.Load(topic.macaddr, topic.sensorid)
        else:
            icpe.Verify(topic, payload, mqttsrc)
            zinfo = zwave.db.SensorInfo(payload['vid'], payload['pid'])
            SensorSQL.Create(topic.macaddr, topic.sensorid, zinfo)
            SensorRedis.Load(topic.macaddr, topic.sensorid)
    
    return mqtt.sensor.Query(topic.macaddr, topic.sensorid, **mqttsrc)
