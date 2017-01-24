from ..SQL import iCPEModel, SensorModel, SensorClassModel
from ... import db

def Create(icpe, sensorid):
    if type(icpe) is str:
        icpe = iCPEModel.query.filter_by(mac = icpe).first()
        if icpe is None:
            raise LookupError('iCPE not found')
    sensor = SensorModel(sensorid)
    icpe.sensors.append(sensor)
    db.session.add(icpe, sensor)
    db.session.commit()
    logger.info("Created Sensor {}:{}".format(icpe.mac, sensor.sensorid))
    return sensor

def Delete(sensor, icpe = None):
    if type(sensor) is str and icpe:
        sensor = SensorModel.query.join(iCPEModel).\
                filter(SensorModel.sensorid == sensor).\
                filter(iCPEModel.mac == icpe).first()

        if sensor is None:
            raise LookupError('Sensor not found')

    db.session.delete(sensor)
    db.session.commit()
    logger.info("Deleted Sensor {}:{}".format(icpe.mac, sensor.sensorid))
    return sensor

def Save(sensor):
    db.session.add(sensor)
    db.session.commit()
    return sensor

def List(icpe = None):
    if icpe is None:
        return [sensor for sensor in SensorModel.query.all()]
    if type(icpe) is str:
        icpe = iCPEModel.query.filter_by(mac = icpe).first()
        if icpe is None:
            raise LookupError('iCPE not found')
    return [sensor for sensor in icpe.sensors]

def Get(icpe, sensor):
    return SensorModel.query.join(iCPEModel).\
                filter(SensorModel.sensorid == int(sensor)).\
                filter(iCPEModel.mac == icpe).first()

def AddClass(mac, sensorid, classnumber, classname):
    print('Add Class: ' + mac + str(sensorid))
    s = SensorClassModel.query.join(SensorModel).join(iCPEModel).\
       filter(SensorClassModel.classnumber == str(classnumber)).\
       filter(SensorModel.sensorid == int(sensorid)).\
       filter(iCPEModel.mac == str(mac)).first()

    sensor = Get(mac, sensorid)
    cmdclass = SensorClassModel(classnumber, classname)
    sensor.cmdclasses.append(sensor, cmdclass)
    db.session.add(sensor)
    db.session.commit()
    logger.info("Added Class {} to Sensor {}:{}".format(classname, mac,
                                                        sensorid))
    return sensor

def AddClassTypes(mac, sensorid, classname, classtypes):
    cmdclass = SensorClassModel.query.join(SensorModel).join(iCPEModel).\
       filter(SensorClassModel.classname == classname).\
       filter(SensorModel.sensorid == sensorid).\
       filter(iCPEModel.mac == mac).first()

    if cmdclass is None:
        return False

    cmdclass.classtypes = classtypes
    db.session.add(cmdclass)
    db.session.commit()
    logger.info("Added Classtypes {}:{} to Sensor {}:{}".\
                format(classname, classtypes, mac, sensorid))
    return cmdclass
