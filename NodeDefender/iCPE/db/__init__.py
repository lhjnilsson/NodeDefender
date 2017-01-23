from redis import ConnectionPool, StrictRedis
from functools import wraps

pool = ConnectionPool(host='localhost', port=6379, db=0)


def redisconn(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        conn = StrictRedis(connection_pool=pool)
        return func(*args, conn = conn, **kwargs)
    return wrapper

@celery.task
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

from . import sensor, icpe
