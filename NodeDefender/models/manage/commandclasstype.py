from ..SQL import iCPEModel, SensorModel, CommandClassModel,\
CommandClassTypeModel
from ... import db
from . import logger

def List(macaddr = None, sensorid = None, commandclass = None):
    return db.session.query(CommandClassTypeModel).all()

def Get(macaddr, sensorid, classnumber, classtype):
    return db.session.query(CommandClassTypeModel).\
            join(CommandClassTypeModel.commandclass).\
            join(CommandClassModel.sensor).\
            join(SensorModel.icpe).\
            filter(iCPEModel.macaddr == macaddr).\
            filter(SensorModel.sensorid == sensorid).\
            filter(CommandClassModel.number == classnumber).\
            filter(CommandClassTypeModel.number == classtype).first()

def Add(macaddr, sensorid, classnumber, classtype):
    commandclasstype =  Get(macaddr, sensorid, classnumber, classtype)
    if commandclasstype:
        return commandclasstype

    commandclass = db.session.query(CommandClassModel).\
            join(CommandClassModel.sensor).\
            join(SensorModel.icpe).\
            filter(iCPEModel.macaddr == macaddr).\
            filter(SensorModel.sensorid == sensorid).\
            filter(CommandClassModel.number == classnumber).first()
    
    if commandclass is None:
        raise TypeError('Command Class does not exist')

    commandclasstype = CommandClassTypeModel(classtype)

    commandclass.types.append(commandclasstype)
    db.session.add(commandclass, commandclasstype)
    db.session.commit()
    logger.info("Added Classtype {} to Sensor {}:{}".\
                format(classtype, macaddr, sensorid))
    return commandclasstype

def Save(commandclasstype):
    db.session.add(commandclasstype)
    return db.session.commit()
