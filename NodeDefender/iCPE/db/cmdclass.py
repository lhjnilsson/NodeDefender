from ...models.manage import cmdclass as CmdclassSQL
from ...models.redis import cmdclass as CmdclassRedis
from ...models.manage import field as FieldSQL
from ...models.redis import field as FieldRedis
from . import redisconn
from .. import mqtt, zwave
from ... import celery
from datetime import datetime
from .. import logger
from ..decorators import ParsePayload

@ParsePayload
def Verify(topic, payload, mqttsrc = None):
    if len(CmdclassRedis.Get(topic.macaddr, topic.sensorid, topic.cmdclass)):
        return True
    cmdclass = CmdclassSQL.Get(topic.macaddr, topic.sensorid, payload.cls)
    if cmdclass and cmdclass.supported:
        CmdclassRedis.Load(topic.macaddr, topic.sensorid, topic.cmdclass)
        return True

    if cmdclass and not cmdclass.supported:
        return True
    
    print("{}{}{} not found".format(topic.macaddr, topic.sensorid,
                                    payload.cls))
    return Add(topic, payload)

# Takes Cmdclass SQL Model and updated the fields
def Update(cmdclass):
    if cmdclass.supported:
        FieldSQL.Clear(cmdclass.sensor.icpe.macaddr,
                          cmdclass.sensor.sensorid, cmdclass.classnumber)

    classinfo = zwave.Info(cmdclass.classnumber)
    if not classinfo:
        return

    cmdclass.classname = classinfo.classname
    cmdclass.supported = True
    CmdclassSQL.Save(cmdclass)
    CmdclassRedis.Load(cmdclass)
    if classinfo.types:
        mqtt.sensor.Sup(cmdclass.sensor.icpe.macaddr,
                        cmdclass.sensor.sensorid, cmdclass.classname)

    for field in classinfo.fields:
        if not len(field):
            continue
        FieldRedis.Load(FieldSQL.Add(cmdclass.sensor.icpe.macaddr,\
                                     cmdclass.sensor.sensorid,\
                                     classinfo.classname,\
                                     **field))

@ParsePayload
def Add(topic, payload, mqttsrc = None):
    try:
        cmdclasses = payload.clslist_0.split(',')
    except AttributeError:
        cmdclasses = [payload.cls]
    
    for cmdclass in cmdclasses:
        cls = CmdclassSQL.Add(topic.macaddr, topic.sensorid, cmdclass)

        classinfo = zwave.Info(cmdclass)
        if not classinfo:
            continue
        if classinfo.types:
            mqtt.sensor.Sup(topic.macaddr, topic.sensorid,
                            classinfo.classname)

        cls.classname = classinfo.classname
        cls.supported = True
        CmdclassSQL.Save(cls)
        
        for field in classinfo.fields:
            if not len(field):
                continue
            FieldRedis.Load(FieldSQL.Add(topic.macaddr, topic.sensorid,\
                                     classinfo.classname, **field))
        CmdclassRedis.Load(topic.macaddr, topic.sensorid, classinfo.classname)

    return True

@ParsePayload
def AddTypes(topic, payload, mqttsrc = None):
    try:
        types = payload.typelist.split(',')
    except AttributeError:
        types = list(payload.type)

    CmdclassSQL.AddTypes(topic.macaddr, topic.sensorid, payload.cls,
                         types)

    for classtype in types:
        classinfo = zwave.Info(payload.cls, classtype)
        if not classinfo:
            print('no classinfo..')
            continue
        print('adding field', classinfo)
        for field in classinfo.fields:
            if not len(field):
                continue
            FieldRedis.Load(FieldSQL.Add(topic.macaddr, topic.sensorid,
                                         classinfo.classname, **field))
             
    return CmdclassRedis.Load(topic.macaddr, topic.sensorid, payload.cls)
