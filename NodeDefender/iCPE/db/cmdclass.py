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
    
    icpe.Verify(topic, payload, mqttsrc)
    sensor.Verify(topic, payload, mqttsrc)
    return Add(topic, payload)

@ParsePayload
def Add(topic, payload):
    try:
        cmdclasses = payload.clslist_0
    except AttributeError:
        cmdclasses = list(payload.cls[-2:])

    for cmdclass in cmdclasses:
        cls = CmdclassSQL.Add(topic.macaddr, topic.sensorid, cmdclass)

        classinfo = zwave.Info(topic.cmdclass)
        if not classinfo:
            continue
        if classinfo.types:
            mqtt.sensor.Sup(topic.macaddr, topic.sensorid,
                            classinfo.classname)

        cls.classname = classinfo.classname
        cls.supported = True

        for field in classinfo.fields:
            if not len(field):
                continue
            FieldRedis.Load(FieldSQL.Add(topic.macaddr, topic.sensorid,\
                                     classinfo.classname, **field))
        CmdclassRedis.Load(topic.macaddr, topic.sensorid, classinfo.classname)
        CmdclassSQL.Save(cls)

    return True

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
