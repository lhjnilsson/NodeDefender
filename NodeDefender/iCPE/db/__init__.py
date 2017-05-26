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

def Load(mqttsrc, mac, sensorid = None):
    if sensorid:
        if sensor.Load(mac, sensorid):
            pass
        else:
            if icpe.Load(mac):
                sensor.CreateLoadQuery(mqttsrc, mac, sensorid)
            else:
                icpe.CreateLoadQuery(mqttsrc, mac)
                sensor.CreateLoadQuery(mqttsrc, mac, sensorid)

    else:
        if icpe.Load(mac):
            pass
        else:
            icpe.CreateLoadQuery(mqttsrc, mac)

    return sensor.Get(mac, sensorid) if sensorid else icpe.Get(mac)

from . import sensor, icpe, commandclass
