from ..SQL import iCPEModel, SensorModel, CommandClassModel
from ... import db
from . import logger

def Get(mac, sensorid, classnumber):
    return db.session.query(CommandClassModel).\
            join(CommandClassModel.sensor).\
            filter(SensorModel.sensorid == sensorid).\
            filter(CommandClassModel.classnumber == classnumber).first()

def Add(mac, sensorid, classnumber):
    commandclass = Get(mac, sensorid, classnumber)
    if commandclass:
        return commandclass

    s = sensor.Get(mac, sensorid)
    if s is None:
        print('Sensor {} not found'.format(sensorid))
    commandclass = CommandClassModel(classnumber)
    s.commandclasses.append(commandclass)
    db.session.add(s, commandclass)
    db.session.commit()
    logger.info("Added Class {} to Sensor {}:{}".format(classnumber, mac,\
                                                        sensorid))
    return commandclass

def Save(commandclass):
    db.session.add(commandclass)
    return db.session.commit()
