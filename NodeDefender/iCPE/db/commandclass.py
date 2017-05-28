from ...models.manage import commandclass as CommandclassSQL
from ...models.redis import commandclass as CommandclassRedis
from . import field as FieldDB
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
        if not classinfo.fields:
            continue

        for field in classinfo.fields:
            if not len(field):
                continue
            FieldRedis.Load(FieldSQL.Add(topic.macaddr, topic.sensorid,\
                                     classinfo.name, **field))
        CommandclassRedis.Load(topic.macaddr, topic.sensorid, classinfo.name)

    FieldDB.Load(topic.sensorid)
    return True

@celery.task
def Load(sensor = None):
    for commandclass in CommandclassSQL.List(sensor):
        CommandclassRedis.Load(commandclass)
    return True
