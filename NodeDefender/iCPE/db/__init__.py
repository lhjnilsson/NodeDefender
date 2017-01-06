from . import *
from redis import ConnectionPool

pool = ConnectionPool(host='localhost', port=6379, db=0)

def Load(mac, sensorid = None):
    if sensorid:
        if sensor.Load(mac, sensorid):
            pass
        else:
            if icpe.Load(mac):
                sensor.Create(mac, sensorid)
            else:
                icpe.Create(mac)
                sensor.Create(mac, sensorid)

    else:
        if icpe.Load(mac):
            pass
        else:
            icpe.Create(mac)

    return True
