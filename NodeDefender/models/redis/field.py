from ... import celery
from datetime import datetime
from . import logger
from . import redisconn

@redisconn
def Load(field, conn):
    if field is None:
        return None
    f = {
        'name' : field.name,
        'macaddr' : field.icpe.macaddr,
        'sensorid' : field.sensor.sensorid,
        'cmdclass' : field.sensorclass.classname,
        'type' : field.type,
        'readonly' : field.readonly,
        'display' : field.display,
        'loaded_at' : str(datetime.now())
    }
    conn.sadd(field.icpe.macaddr + field.sensor.sensorid + ':fields',
              field.name)
    conn.hmset(field.icpe.macaddr + field.sensor.sensorid + field.name, f)
    return f

@redisconn
def Update(mac, sensorid, name, value, conn):
    print(mac, sensorid, name, value)
    conn.hmset(mac + sensorid + name, {'value' : str(value)})
    conn.hmset(mac + sensorid + name, {'last_updated' : str(datetime.now())})
    return conn.hgetall(mac + sensorid + name)

@redisconn
def Get(mac, sensorid, name, conn):
    return conn.hgetall(mac + sensorid + name)

def Remove():
    pass
