from ...models.manage import cmdclass as CmdclassSQL
from ...models.redis import cmdclass as CmdclassRedis
from ...models.manage import field as FieldSQL
from ...models.redis import field as FieldRedis
from . import redisconn, icpe, sensor
from .. import mqtt, zwave
from ... import celery
from datetime import datetime
from .. import logger

def Verify(topic, payload, mqttsrc = None):
    if len(CmdclassRedis.Get(topic.macaddr, topic.sensorid, topic.cmdclass)):
        return True
    
    if CmdclassRedis.Load(topic.macaddr, topic.sensorid, topic.cmdclass):
        return True

    if not zwave.Supported(topic.cmdclass):
        return False
    
    icpe.Verify(topic, payload, mqttsrc)
    sensor.Verify(topic, payload, mqttsrc)
    return Add(topic, payload)

def Add(topic, payload, classnum = None):
    if classnum:
        try:
            topic.cmdclass = zwave.NumToName(classnum)
        except NotImplementedError:
            return False
    try:
        classinfo = zwave.Info(topic.cmdclass)
    except NotImplementedError:
        return False
    
    if classinfo.types:
        mqtt.sensor.Sup(topic.macaddr, topic.sensorid, classinfo.classname)

    CmdclassSQL.Add(topic.macaddr, topic.sensorid, classinfo.classnumber,
                    classinfo.classname)
    for field in classinfo.fields:
        if not len(field):
            continue
        FieldRedis.Load(FieldSQL.Add(topic.macaddr, topic.sensorid, classinfo.classname,
                            **field))
    return CmdclassRedis.Load(topic.macaddr, topic.sensorid, classinfo.classname)

def AddTypes(topic, payload):
    try:
        types = payload.typelist.split(',')
    except AttributeError:
        types = payload.type

    CmdclassSQL.AddTypes(topic.macaddr, topic.sensorid, topic.cmdclass,
                         types)
    for classtype in types:
        try:
            classinfo = zwave.Info(topic.cmdclass, classtype)
        except NotImplementedError:
            pass

        for field in classinfo.fields:
            if not len(field):
                continue
            FieldRedis.Load(FieldSQL.Add(topic.macaddr, topic.sensorid,
                                topic.cmdclass, **field))
             
    return CmdclassRedis.Load(topic.macaddr, topic.sensorid, topic.cmdclass)
