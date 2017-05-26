from ...models.manage import commandclass as CommandclassSQL
from ...models.redis import commandclass as CommandclassRedis
from ...models.redis import field as FieldRedis
from . import redisconn
from .. import mqtt, zwave
from ... import celery
from datetime import datetime
from .. import logger
from ..decorators import ParsePayload

@ParsePayload
def Verify(topic, payload, mqttsrc = None):
    if len(CommandclassRedis.Get(topic.macaddr, topic.sensorid, topic.commandclass)):
        return True
    commandclass = CommandclassSQL.Get(topic.macaddr, topic.sensorid, payload.cls)
    if commandclass and commandclass.supported:
        CommandclassRedis.Load(topic.macaddr, topic.sensorid, topic.commandclass)
        return True

    if commandclass and not commandclass.supported:
        return True
    
    print("{}{}{} not found".format(topic.macaddr, topic.sensorid,
                                    payload.cls))
    return Add(topic, payload)

# Takes Commandclass SQL Model and updated the fields
def Update(commandclass):
    classinfo = zwave.Info(commandclass.number)
    if not classinfo:
        return

    commandclass.name = classinfo.name
    commandclass.supported = True
    CommandclassSQL.Save(commandclass)
    CommandclassRedis.Load(commandclass)
    if classinfo.types:
        mqtt.sensor.Sup(commandclass.sensor.icpe.macaddr,
                        commandclass.sensor.sensorid, commandclass.name)

    for field in classinfo.fields:
        if not len(field):
            continue
        FieldRedis.Load(commandclass.sensor.icpe.macaddr,\
                                     commandclass.sensor.sensorid,\
                                     classinfo.name,\
                                     **field)

@ParsePayload
def Add(topic, payload, mqttsrc = None):
    try:
        commandclasses = payload.clslist_0.split(',')
    except AttributeError:
        commandclasses = [payload.cls]
    
    for commandclass in commandclasses:
        cls = CommandclassSQL.Add(topic.macaddr, topic.sensorid, commandclass)

        classinfo = zwave.Info(commandclass)
        if not classinfo:
            continue
        if classinfo.types:
            mqtt.sensor.Sup(topic.macaddr, topic.sensorid,
                            classinfo.name)

        cls.name = classinfo.name
        cls.supported = True
        CommandclassSQL.Save(cls)
        
        for field in classinfo.fields:
            if not len(field):
                continue
            FieldRedis.Load(FieldSQL.Add(topic.macaddr, topic.sensorid,\
                                     classinfo.name, **field))
        CommandclassRedis.Load(topic.macaddr, topic.sensorid, classinfo.name)

    return True

@ParsePayload
def AddTypes(topic, payload, mqttsrc = None):
    try:
        types = payload.typelist.split(',')
    except AttributeError:
        types = list(payload.type)

    CommandclassSQL.AddTypes(topic.macaddr, topic.sensorid, payload.cls,
                         types)

    for classtype in types:
        try:
            t = CommandclassSQL.AddType(topic.macaddr, topic.sensorid, payload.cls,
                                    classtype)
        except KeyError:
            continue

        t_info = zwave.Info(payload.cls, classtype)
        if not t_info:
            continue

        t.name = t_info.name
        t.supported = True
        CommandclassSQL.UpdateType(t)
        FieldRedis.Load(t)

    return CommandclassRedis.Load(topic.macaddr, topic.sensorid, payload.cls)
