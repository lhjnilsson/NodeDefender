from NodeDefender.db.sql import SQL, iCPEModel, SensorModel,\
                                CommandClassModel, CommandClassTypeModel
from NodeDefender.db import logger
import NodeDefender

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
    sensor = NodeDefender.db.sensor.get_sql(macaddr, sensorid)
    if sensor is None:
        return False
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

def get(macaddr, sensorid, classnumber = None, classname = None):
    cc = get_sql(macaddr, sensorid, classnumber = classnumber, \
                 classname = classname)
    if cc:
        return cc.to_json()
    else:
        return False

def update(macaddr, sensorid, classnumber = None, classname = None, **kwargs):
    return update_sql(macaddr, sensorid, classnumber = classnumber, \
                      classname = classname, **kwargs)

def list(macaddr, sensorid):
    sensor = NodeDefender.db.sensor.get_sql(macaddr, sensorid)
    if not sensor:
        return []
    return [commandclass.to_json() for commandclass in sensor.commandclasses]

def number_list(macaddr, sensorid):
    sensor = NodeDefender.db.sensor.get_sql(macaddr, sensorid)
    if sensor:
        return [c.number for c in sensor.commandclasses]
    else:
        return []

def create(macaddr, sensorid, classnumber):
    if not create_sql(macaddr, sensorid, classnumber):
        return False
    info = NodeDefender.icpe.zwave.commandclass.info(classnumber = classnumber)
    if info:
        update(macaddr, sensorid, classnumber = classnumber, **info)
        if info['types']:
            NodeDefender.mqtt.command.commandclass.sup(macaddr, sensorid, \
                                                       info['name'])
    return get(macaddr, sensorid, classnumber = classnumber)

def delete(macaddr, sensorid, classnumber = None, classname = None):
    return delete_sql(macaddr, sensorid, classnumber = classnumber, \
                      classname = classname)

def verify_list(macaddr, sensorid, classList):
    knownClasses = number_list(macaddr, sensorid)
    for classnumber in classList.split(','):
        if classnumber not in knownClasses:
            create(macaddr, sensorid, classnumber = classnumber)

    for classnumber in knownClasses:
        if classnumber not in classList:
            delete(macaddr, sensorid, classnumber = classnumber)

    return True

def add_types(macaddr, sensorid, classname, classtypes):
    commandclass = get_sql(macaddr, sensorid, classname = classname)
    if commandclass is None:
        return False
    for classtype in classtypes:
        typeModel = CommandClassTypeModel(classtype)
        info = zwave.commandclass.info(classname = classname,\
                                       classtype = classtype)
        typeModel.name = info['name']
        typeModel.supported = info['supported']
        typeModel.web_field = info['webField']
        db.session.save(typeModel)
        db.session.commit()
    return True
