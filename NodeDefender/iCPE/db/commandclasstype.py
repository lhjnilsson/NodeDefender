from ...models.manage import commandclasstype as CommandclasstypeSQL
from ...models.redis import commandclass as CommandclassRedis
from ...models.redis import field as FieldRedis
from . import field as FieldDB
from . import redisconn
from .. import mqtt, zwave
from ... import celery
from datetime import datetime
from .. import logger
from ..decorators import ParsePayload

@ParsePayload
def Add(topic, payload, mqttsrc = None):
    print('adding type...')
    try:
        types = payload.typelist.split(',')
    except AttributeError:
        types = list(payload.type)

    for classtype in types:
        try:
            t = CommandclasstypeSQL.Add(topic.macaddr, topic.sensorid, payload.cls,
                                    classtype)
        except KeyError:
            continue

        t_info = zwave.Info(payload.cls, classtype)
        if not t_info:
            print('ERROR FINDING TYPE', payload.cls, classtype)

        t.name = t_info.name
        t.number = t_info.number
        t.fields = t_info.fields
        t.supported = True
        CommandclasstypeSQL.Save(t)
    
    FieldDB.Load(topic.sensorid)
    return CommandclassRedis.Load(topic.macaddr, topic.sensorid, payload.cls)

@celery.task
def Load(commandclass = None):
    #for commandclasstype in CommandclasstypeSQL.List(commandclass):
        #CommandclassRedis.Load(commandclasstype)
    return True
