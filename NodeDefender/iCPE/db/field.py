from ...models.redis import field as FieldRedis
from ...models.manage import commandclass as CommandclassSQL
from . import redisconn
from datetime import datetime
from .. import celery, zwave

def Update(topic, data):
    return FieldRedis.Update(topic.macaddr, topic.sensorid, **data)

@celery.task
def Load(sensor = None):
    for commandclass in CommandclassSQL.List(sensor):
        if not commandclass.name:
            continue

        types = commandclass.types
        if types:
            for t in types:
                if not t.name:
                    continue
                try:
                    field = eval('zwave.commandclass.'+commandclass.name+'.'+\
                                t.name+'.Fields')()
                except AttributeError:
                    print(commandclass.name, t.name)
                if field:
                    FieldRedis.Load(commandclass, field)
            continue
        else:
            field = eval('zwave.commandclass.'+commandclass.name+\
                         '.Fields')()
            if field:
                FieldRedis.Load(commandclass, field)

