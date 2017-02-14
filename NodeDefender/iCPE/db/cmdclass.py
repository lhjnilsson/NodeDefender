from ...models.manage import cmdclass as CmdclassSQL
from ...models.redis import cmdclass as CmdclassRedis
from . import redisconn, icpe, sensor
from .. import mqtt, zwave
from ... import celery
from datetime import datetime
from .. import logger


def Verify(topic, payload, mqttsrc = None):
    if len(CmdclassRedis.Get(topic.macaddr, topic.sensorid, topic.cmdclass)):
        return CmdclassRedis.Get(topic.macaddr, topic.sensorid, topic.cmdclass)
    
    elif CmdclassSQL.Get(topic.macaddr, topic.sensorid, topic.cmdclass):
        return CmdclassRedis.Load(topic.macaddr, topic.sensorid, topic.cmdclass)
    
    else:
        if not zwave.Supported(topic.cmdclass):
            return False
        icpe.Verify(topic, payload, mqttsrc)
        sensor.Verify(topic, payload, mqttsrc)

    return mqtt.sensor.Query(topic.macaddr, topic.sensorid, **mqttsrc)

def Add(topic, payload, *classes):
    sensor.Verify(topic, payload)
    for classnum in classes:
        try:
            classname, types, fields = zwave.Info(classnum)
        except TypeError:
            print("Error adding class ", classnum)
            return False
        
        if classname is None:
            break

        if types:
            mqtt.sensor.Sup(topic.macaddr, topic.sensorid, classname)

        CmdclassSQL.Add(topic.macaddr, topic.sensorid, classnum, classname)
        if fields:
            CmdclassSQL.AddField(topic.macaddr, topic.sensorid, classname, **fields)
        CmdclassRedis.Load(topic.mac, topic.sensorid, classname)
    return True

def AddTypes(topic, payload, classname, classtypes):
    sensor.Verify(topic.macaddr, topic.sensorid)
    CmdclassSQL.AddTypes(topic.macaddr, topic.sensorid, classname, classtypes)
    fields = zwave.InfoTypes(classname, classtypes)
    if fields:
        for field in fields:
            CmdclassSQL.AddField(topic.macaddr, topic.sensorid, classname, **field)
    return CmdclassRedis.Load(topic.macaddr, topic.sensorid, classname)
