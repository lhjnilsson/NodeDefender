from redis import ConnectionPool, StrictRedis
from functools import wraps
from ... import logger, RedisPool


def Verify(topic, payload, mqttsrc):
    icpe.Verify(topic, payload, mqttsrc)
    sensor.Verify(topic, payload, mqttsrc)
    commandclass.Verify(topic, payload, mqttsrc)
    return True

def redisconn(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        conn = StrictRedis(connection_pool=pool)
        return func(*args, conn = conn, **kwargs)
    return wrapper

def Load(*args):
    icpe.Load.apply_async()
    sensor.Load.apply_async()
    commandclass.Load.apply_async()
    commandclasstype.Load.apply_async()
    field.Load.apply_async()

from . import sensor, icpe, commandclass, commandclasstype, field
