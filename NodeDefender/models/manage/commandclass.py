from ..SQL import iCPEModel, SensorModel, CommandClassModel
from ... import db
from . import logger

def List(sensorid = None):
    if sensorid:
        return db.session.query(CommandClassModel).\
                join(CommandClassModel.sensor).\
                filter(SensorModel.sensorid == sensorid).all()
    return db.session.query(CommandClassModel).all()

def Get(mac, sensorid, classnumber):
    return db.session.query(CommandClassModel).\
            join(CommandClassModel.sensor).\
            filter(SensorModel.sensorid == sensorid).\
            filter(CommandClassModel.number == classnumber).first()

def Add(macaddr, sensorid, classnumber):
    commandclass = Get(macaddr, sensorid, classnumber)
    if commandclass:
        return commandclass

    s = db.session.query(SensorModel).\
            join(SensorModel.icpe).\
            filter(iCPEModel.macaddr == macaddr).\
            filter(SensorModel.sensorid == sensorid).first()
    
    if s is None:
        print('Sensor {}:{} not found'.format(macaddr, sensorid))

    commandclass = CommandClassModel(classnumber)
    s.commandclasses.append(commandclass)
    db.session.add(s, commandclass)
    db.session.commit()
    logger.info("Added Class {} to Sensor {}:{}".format(classnumber, macaddr,\
                                                        sensorid))
    return commandclass

def Save(commandclass):
    db.session.add(commandclass)
    return db.session.commit()
