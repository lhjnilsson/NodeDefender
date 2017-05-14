from ..SQL import iCPEModel, SensorModel, SensorClassModel, FieldModel
from ... import db
from . import logger, sensor

def Get(mac, sensorid, classnumber):
    s = sensor.Get(mac, sensorid)
    if s is None:
        return False
    
    return db.session.query(SensorClassModel).\
            join(SensorClassModel.sensor).\
            filter(SensorModel.id == s.id).\
            filter(SensorClassModel.classnumber == classnumber).first()

def Add(mac, sensorid, classnumber):
    cmdclass = Get(mac, sensorid, classnumber)
    if cmdclass:
        return cmdclass

    s = sensor.Get(mac, sensorid)
    if s is None:
        print('Sensor {} not found'.format(sensorid))
    cmdclass = SensorClassModel(classnumber)
    s.cmdclasses.append(cmdclass)
    db.session.add(s, cmdclass)
    db.session.commit()
    logger.info("Added Class {} to Sensor {}:{}".format(classnumber, mac,\
                                                        sensorid))
    return cmdclass

def Save(cmdclass):
    db.session.add(cmdclass)
    db.session.commit()

def AddTypes(mac, sensorid, classnumber, classtypes):
    cmdclass = Get(mac, sensorid, classnumber)

    if cmdclass is None:
        return False

    cmdclass.classtypes = str(classtypes)
    db.session.add(cmdclass)
    db.session.commit()
    logger.info("Added Classtypes {} to Sensor {}:{}".\
                format(classtypes, mac, sensorid))
    return cmdclass
