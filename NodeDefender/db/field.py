from NodeDefender.db import redis
from NodeDefender.db.sql import SQL, CommandClassModel, CommandClassTypeModel
import NodeDefender

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
    commandclasses = SQL.session.query(CommandClassModel).\
                    filter(CommandClassModel.name.isnot(None)).all()
    if len(commandclasses):
        load_commandclass(*commandclasses)

    commandclasstypes = SQL.session.query(CommandClassTypeModel).\
                 filter(CommandClassTypeModel.name.isnot(None)).all()
    if len(commandclasstypes):
        load_commandclasstype(*commandclasstypes)

    return len(commandclasses) + len(commandclasstypes)

def load_from_icpe(icpe):
    for sensor in icpe.sensors:
        load_from_sensor(sensor)

def load_from_sensor(sensor):
    load_commandclass(sensor.commandclasses)

def load_commandclass(*commandclasses):
    for commandclass in commandclasses:
        field = eval('NodeDefender.icpe.zwave.commandclass.'+\
                     commandclass.name+'.fields')
        if field:
            redis.field.load(commandclass.sensor, **field)
        if commandclass.types:
            load_commandclasstype(*commandclass.types)
    return len(commandclasses)

def load_commandclasstype(*cctypes):
    for cctype in cctypes:
        field = eval('NodeDefender.icpe.zwave.commandclass.'+\
                     cctype.commandclass.name+'.'+cctype.name+'.fields')
        if field:
            redis.field.load(cctype.commandclass.sensor, **field)

    return len(cctypes)

def flush(macaddr, sensorid, name):
    return delete_redis(macaddr, sensorid, name)
