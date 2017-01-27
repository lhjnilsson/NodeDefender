from ...models.manage import cmdclass as CmdclassSQL
from ...models.redis import cmdclass as CmdclassRedis
from . import redisconn, icpe, sensor
from .. import mqtt, zwave
from ... import celery
from datetime import datetime
from .. import logger

@celery.task
def Add(mac, sensorid, *classes):
    sensor.Verify(mac, sensorid)
    for classnum in classes:
        try:
            classname, types = zwave.Info(classnum)
        except TypeError:
            print("Error adding class ", classnum)
            return

        if types:
            mqtt.sensor.Sup(mac, sensorid, classname)

        CmdclassSQL.Add(mac, sensorid, classnum, classname)
    
    return CmdclassRedis.Load(mac, sensorid, classname)

@celery.task
def AddTypes(mac, sensorid, cmdclass, classtypes):
    sensor.Verify(mac, sensorid)
    SensorSQL.AddClassTypes(mac, sensorid, classname, classtypes)
    return Load(mac, sensorid)
