from ...models.manage import sensor as SensorSQL
from ...models.redis import sensor as SensorRedis
from . import redisconn, icpe
from .. import mqtt, zwave
from ... import celery
from datetime import datetime
from .. import logger

@celery.task
def Verify(mac, sensorid, ipaddr = None, port = None):
    if len(SensorRedis.Get(mac, sensorid)):
        return SensorRedis.Get(mac, sensorid)
    else:
        if SensorSQL.Get(mac, sensorid):
            return SensorRedis.Load(SensorSQL.Get(mac, sensorid))
        else:
            icpe.Verify(mac, ipaddr, port)
            SensorSQL.Create(mac, sensorid)
            SensorRedis.Load(SensorSQL.Get(mac, sensorid))
    
    return mqtt.sensor.Query(mac, sensorid, ipaddr, port)
