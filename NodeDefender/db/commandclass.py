from NodeDefender.db.sql import SQL, iCPEModel, SensorModel, CommandClassModel
from NodeDefender.db import redis, logger
from NodeDefender import db, mqtt
from NodeDefender.icpe import zwave

def get_sql(macaddr, sensorid, classnumber = None, classname = None):
    if classnumber is None and classname is None:
        raise TypeError('Please enter either classnumber or classname')
    if classnumber:
        return SQL.session.query(CommandClassModel).\
                join(CommandClassModel.sensor).\
                join(SensorModel.icpe).\
                filter(iCPEModel.macaddr == macaddr).\
                filter(SensorModel.sensorid == sensorid).\
                filter(CommandClassModel.number == classnumber).first()
    elif classname:
        return SQL.session.query(CommandClassModel).\
                join(CommandClassModel.sensor).\
                join(SensorModel.icpe).\
                filter(iCPEModel.macaddr == macaddr).\
                filter(SensorModel.sensorid == sensorid).\
                filter(CommandClassModel.name == classname).first()

def update_sql(macaddr, sensorid, classnumber = None, classname = None, **kwargs):
    if classnumber:
        commandclass = get_sql(macaddr, sensorid, classnumber = classnumber)
    elif classname:
        commandclass = get_sql(macaddr, sensorid, classname = classname)
    else:
        raise TypeError('Please enter either classnumber or classname')

    if commandclass is None:
        return False

    columns = commandclass.columns()
    for key, value in kwargs.items():
        if key not in columns:
            continue
        setattr(commandclass, key, value)

    SQL.session.add(commandclass)
    SQL.session.commit()
    return commandclass

def create_sql(macaddr, sensorid, classnumber = None, classname = None):
    if classnumber:
        commandclass = get_sql(macaddr, sensorid, classnumber = classnumber)
    elif classname:
        commandclass = get_sql(macaddr, sensorid, classname = classname)
    else:
        raise TypeError('Please enter either classnumber or classname')
    
    if commandclass:
        return commandclass

    commandclass = CommandClassModel(classnumber, classname)
    sensor = db.sensor.get_sql(macaddr, sensorid)
    sensor.commandclasses.append(commandclass)
    SQL.session.add(sensor, commandclass)
    SQL.session.commit()
    logger.debug("Created SQL Entry for {!r}:{!r}:{!r}".\
                 format(macaddr, sensorid, commandclass.number))
    return commandclass

def delete_sql(macaddr, sensorid, classnumber = None, classname = None):
    if classnumber:
        commandclass = get_sql(macaddr, sensorid, classnumber = classnumber)
    elif classname:
        commandclass = get_sql(macaddr, sensorid, classname = classname)
    else:
        raise TypeError('Please enter either classnumber or classname')

    if commandclass is None:
        return False
    SQL.session.delete(commandclass)
    logger.debug("Deleted SQL Entry for {!r}:{!r}:{!r}".\
                 format(macaddr, sensorid, commandclass.number))
    return SQL.session.commit()

def get_redis(macaddr, sensorid, classname):
    return redis.commandclass.get(macaddr, sensorid, classname)

def update_redis(macaddr, sensorid, classname, **kwargs):
    return redis.commandclass.save(macaddr, sensorid, classname, **kwargs)

def delete_redis(macaddr, sensorid):
    return redis.commandclass.flush(macaddr, sensorid, classname)

def get(macaddr, sensorid, classnumber = None, classname = None):
    if classnumber and not classname:
        commandclass = get_sql(macaddr, sensorid, classnumber = classnumber)
        if not commandclass:
            return False
        if commandclass and not commandclass.name:
            return commandclass.to_json()
        className = commandclass.name
    elif classname:
        commandclass = get_redis(macaddr, sensorid, classname)
        if len(commandclass):
            return commandclass
        commandclass = get_sql(macaddr, sensorid, classname = classname)
        if redis.commandclass.load(commandclass):
            return get_redis(macaddr, sensorid, classname)
        return False
    else:
        raise ValueError('Please enter either classnumber or classname')

def update(macaddr, sensorid, classnumber = None, classname = None, **kwargs):
    if classnumber and not classname:
        commandclass = update_sql(macaddr, sensorid,\
                                  classnumber = classnumber, **kwargs)
        classname = commandclass.name
    if classname:
        update_redis(macaddr, sensorid, classname, **kwargs)
    return True

def list(macaddr, sensorid):
    commandclasses = redis.commandclass.list(macaddr, sensorid)
    if len(commandclasses):
        return commandclasses
    if len(db.sensor.get_sql(macaddr, sensorid).commandclasses):
        for commandclass in db.sensor.get_sql(macaddr,\
                                              commandclass).commandclasses:
            redis.commandclass.load(commandclass)
        return redis.commandclass.list(macaddr, sensorid)
    return []

def number_list(macaddr, sensorid):
    sensor = db.sensor.get_sql(macaddr, sensorid)
    if sensor:
        return [c.number for c in sensor.commandclasses]
    else:
        return []

def create(macaddr, sensorid, classnumber):
    if not create_sql(macaddr, sensorid, classnumber):
        return False
    info = zwave.commandclass.info(classnumber = classnumber)
    if info:
        update(macaddr, sensorid, classnumber = classnumber, **info)
        if info['types']:
            mqtt.command.commandclass.sup(macaddr, sensorid, info['name'])
        return get_redis(macaddr, sensorid, info['name'])
    return {}

def delete(macaddr, sensorid, classnumber = None, classname = None):
    if classname:
        delete_sql(macaddr, sensorid, classname = classname)
        delete_redis(macaddr, sensorid, classname = classname)
        return True
    elif classnumber:
        delete_sql(macaddr, sensorid, classnumber= classnumber)
        return True
    return False

def verify_list(macaddr, sensorid, classList):
    knownClasses = number_list(macaddr, sensorid)
    for classnumber in classList.split(','):
        if classnumber not in knownClasses:
            create(macaddr, sensorid, classnumber = classnumber)

    for classnumber in knownClasses:
        if classnumber not in classList:
            delete(macaddr, sensorid, classnumber = classnumber)

    return True
