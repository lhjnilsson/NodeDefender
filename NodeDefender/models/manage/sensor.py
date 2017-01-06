from ..SQL import iCPEModel, SensorModel

def Create(icpe, sensorid, vid, ptype, pid):
    if type(icpe) is str:
        icpe = iCPEModel.query.filter_by(mac = icpe).first()
        if icpe is None:
            raise LookupError('iCPE not found')
    sensor = SensorModel(senorid, vid, ptype, pid)
    icpe.sensors.add(sensor)
    db.session.add(icpe)
    db.session.commit()
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
    return sensor

def Save(sensor):
    db.session.add(sensor)
    db.session.commit()

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
                filter(SensorModel.sensorid == sensor).\
                filter(iCPEModel.mac == icpe).first()
