from ..SQL import iCPEModel, SensorModel, CommandClassModel,\
CommandClassTypeModel
from ... import db
from . import logger

def Get(macaddr, sensorid, classnumber, classtype):
    return db.session.query(CommandClassTypeModel).\
            join(CommandClassTypeModel.icpe).\
            join(CommandClassTypeModel.sensor).\
            join(CommandClassTypeModel.commandclass).\
            filter(iCPEModel.macaddr == macaddr).\
            filter(SensorModel.sensorid == sensorid).\
            filter(CommandclassModel.number == classnumber).\
            filter(CommandclassTypeModel.number == classtype).first()

def Add(macaddr, sensorid, classnumber, classtype):
    commandclasstype =  Get(macaddr, sensorid, classnumber, classtype)
    if commandclasstype:
        return commandclasstype

    commandclass = db.session.query(CommandClassModel).\
            join(CommandClassModel.icpe).\
            filter(iCPEModel.macaddr == macaddr).\
            filter(CommandClassModel.number == classnumber).first()
    
    if commandclass is None:
        raise TypeError('Command Class does not exist')

    commandclasstype = CommandClassTypeModel(classnumber)

    commandclass.types.append(commandclasstype)
    db.session.add(commandclass, commandclasstype)
    db.session.commit()
    logger.info("Added Classtypes {} to Sensor {}:{}".\
                format(classtypes, macaddr, sensorid))
    return commandclasstype

def Save(commandclasstype):
    db.session.add(commandclasstype)
    return db.session.commit()
