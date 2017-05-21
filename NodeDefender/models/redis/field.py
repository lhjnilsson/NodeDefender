from ... import celery
from datetime import datetime
from . import logger
from . import redisconn

@redisconn
def Load(sensor, cc, field, conn):
    if field is None:
        return None
    
    f = {
        'name' : field.name,
        'type' : field.type,
        'readonly' : field.readonly,

        'icpe' : sensor.icpe.macaddr,
        'sensor' : sensor.sensorid,
        'cc' : cc.number,
        'ccname' : cc.name,
        
        'last_updated' : None,
        'loaded_at' : str(datetime.now())
    }
    conn.sadd(field.icpe.macaddr + field.sensor.sensorid + ':fields',
              field.name)
    conn.hmset(field.icpe.macaddr + field.sensor.sensorid + field.name, f)
    return f

@redisconn
def Update(event, conn):
    conn.hmset(event.icpe.macaddr + event.sensor.sensorid + event.ccevent,
               {'value' : str(event.value)})
    conn.hmset(event.icpe.macaddr + event.sensor.sensorid + event.ccevent, {'last_updated' : str(datetime.now())})
    return conn.hgetall(event.icpe.macaddr + event.sensor.sensorid +
                        event.ccevent)

@redisconn
def Get(mac, sensorid, name, conn):
    return conn.hgetall(mac + sensorid + name)

def Remove():
    pass
