from . import *
from redis import ConnectionPool
from collections import wraps

pool = ConnectionPool(host='localhost', port=6379, db=0)

def redisconn(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        conn = StrictRedis(connection_pool=pool)
        return func(*args, conn, **kwargs)
    return wrapper


def Load(mac, sensorid = None):
    if sensorid:
        if sensor.Load(mac, sensorid):
            pass
        else:
            if icpe.Load(mac):
                sensor.CreateLoadQuery(mqtt, mac, sensorid)
            else:
                icpe.CreateLoadQuery(mqtt, mac)
                sensor.CreateLoadQuery(mqtt, mac, sensorid)

    else:
        if icpe.Load(mac):
            pass
        else:
            icpe.CreateLoadQuery(mqtt, mac, sensorid)

    return True
