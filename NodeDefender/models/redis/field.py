from ... import celery
from datetime import datetime
from . import logger
from . import redisconn

@redisconn
def Load(commandclass, field, conn):
    if field is None:
        return None
    print(field)
    field = {
        'icpe' : commandclass.sensor.icpe.macaddr,
        'sensor' : commandclass.sensor.sensorid,
        'commandclassNumber' : commandclass.number,
        'commandclassName' : commandclass.name,

        'value' : None,
        
        'last_updated' : None,
        'loaded_at' : str(datetime.now())
    }
    conn.sadd(commandclass.sensor.icpe.macaddr + commandclass.sensor.sensorid\
              + ':fields', field['name'])
    conn.hmset(field.icpe.macaddr + field.sensor.sensorid + field['field'],
               field)
    return f

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
