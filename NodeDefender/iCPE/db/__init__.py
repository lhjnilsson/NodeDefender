from redis import ConnectionPool, StrictRedis
from functools import wraps

pool = ConnectionPool(host='localhost', port=6379, db=0)


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
                sensor.CreateLoadQuery(mac, sensorid)
            else:
                icpe.CreateLoadQuery(mac, **mqtsrc)
                sensor.CreateLoadQuery(mac, sensorid, **mqttsrc)

    else:
        if icpe.Load(mac):
            pass
        else:
            icpe.CreateLoadQuery(mac, **mqttsrc)

    return True

from . import sensor, icpe
