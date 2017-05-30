from ... import celery
from datetime import datetime
from . import logger
from . import redisconn

@redisconn
def Load(commandclass, field, conn):
    if field is None:
        return None
    field['icpe'] = commandclass.sensor.icpe.macaddr
    field['sensor'] = commandclass.sensor.sensorid
    field['commandclassNumber'] = commandclass.number
    field['commandclassName'] = commandclass.name

    field['value'] = None
        
    field['last_updated'] = None,
    field['loaded_at'] = str(datetime.now())
    
    conn.sadd(commandclass.sensor.icpe.macaddr + commandclass.sensor.sensorid\
              + ':fields', field['name'])
    conn.hmset(commandclass.sensor.icpe.macaddr + commandclass.sensor.sensorid\
               + field['name'], field)
    return field

@redisconn
def Update(model, event, conn):
    conn.hmset(model.icpe.macaddr + model.sensor.sensorid + event.field,
               {'value' : str(event.value)})
    conn.hmset(model.icpe.macaddr + model.sensor.sensorid + event.field, {'last_updated' : str(datetime.now())})
    return conn.hgetall(model.icpe.macaddr + model.sensor.sensorid +
                        event.field)

@redisconn
def Get(mac, sensorid, name, conn):
    return conn.hgetall(mac + sensorid + name)

def Remove():
    pass
