from NodeDefender.db import redis
from NodeDefender import db, mqtt
from NodeDefender.icpe import zwave

def get_redis(macaddr, sensorid, name):
    return redis.sensor.get(macaddr, sensorid, name)

def update_redis(macaddr, sensorid, name, **kwargs):
    return redis.sensor.save(macaddr, sensorid, name, **kwargs)

def delete_redis(macaddr, sensorid, name):
    return redis.sensor.flush(macaddr, sensorid, name)

def get(macaddr, sensorid, name):
    return get_redis(macaddr, sensorid, name)

def update(macaddr, sensorid, name, **kwargs):
    return update_redis(macaddr, sensorid, name, **kwargs)

def list(macaddr, sensorid):
    return redis.field.list(macaddr, sensorid)

def load(commandclass, commandclassType = None):
    if commandclassType:
        field = eval('zwave.commandclass.'+commandclass.name+'.'+\
                    commandclassType.name+'.field')()
    else:
        field = eval('zwave.commandclass.'+commandclass.name+'.field')()
    
    if field is None:
        return False
    
    return redis.field.load(commandclass.sensor, **field)

def load_from_sensor(sensor):
    for commandclass in sensor.commandclasses:
        load(commandclass)
        if commandclass.types:
            for commandclasstype in commandclass.types:
                load(commandclass, commandclasstype)

def flush(macaddr, sensorid, name):
    return delete_redis(macaddr, sensorid, name)
