from NodeDefender.db import redis
from NodeDefender.db.sql import SQL, CommandClassModel, CommandClassTypeModel

def get_redis(macaddr, sensorid, name):
    return redis.field.get(macaddr, sensorid, name)

def update_redis(macaddr, sensorid, name, **kwargs):
    return redis.field.save(macaddr, sensorid, name, **kwargs)

def delete_redis(macaddr, sensorid, name):
    return redis.field.flush(macaddr, sensorid, name)

def get(macaddr, sensorid, name):
    return get_redis(macaddr, sensorid, name)

def update(macaddr, sensorid, name, **kwargs):
    return update_redis(macaddr, sensorid, name, **kwargs)

def list(macaddr, sensorid):
    return redis.field.list(macaddr, sensorid)

def load():
    ccs = SQL.session.query(CommandClassModel).\
            filter(CommandClassModel.name.isnot(None)).all()
    for cc in ccs:
        field = eval('NodeDefender.icpe.zwave.commandclass.'+cc.name+'.fields')
        if field:
            redis.field.load(cc.sensor, **field)
    
    cctypes = SQL.session.query(CommandClassTypeModel).\
                 filter(CommandClassTypeModel.name.isnot(None)).all()
    for cctype in cctypes:
        field = eval('NodeDefender.icpe.zwave.commandclass.'+\
                     cctype.commandclass.name+'.'+cctype.name+'.fields')
        if field:
            redis.field.load(cctype.commandclass.sensor, **field)
    
    return len(ccs) + len(cctypes)

def load_from_sensor(sensor):
    for commandclass in sensor.commandclasses:
        load(commandclass)
        if commandclass.types:
            for commandclasstype in commandclass.types:
                load(commandclass, commandclasstype)

def flush(macaddr, sensorid, name):
    return delete_redis(macaddr, sensorid, name)
