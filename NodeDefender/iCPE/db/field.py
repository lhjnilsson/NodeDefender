from ...models.redis import field as FieldRedis
from . import redisconn
from datetime import datetime

def Load(field):
    return FieldRedis.Load(field)

def Update(topic, data):
    return FieldRedis.Update(topic.macaddr, topic.sensorid, **data)
