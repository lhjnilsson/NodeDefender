from ..SQL import iCPEModel, SensorModel, CommandClassModel
from ... import db
from . import logger
from ..manage import message
import NodeDefender.models.redis

def Create(icpe, sensorid, sensorinfo):
    if type(icpe) is str:
        icpe = iCPEModel.query.filter_by(macaddr = icpe).first()
        if icpe is None:
            raise LookupError('iCPE not found')
    sensor = SensorModel(sensorid, sensorinfo)
    icpe.sensors.append(sensor)
    db.session.add(icpe, sensor)
    db.session.commit()
    logger.info("Created Sensor {}:{}".format(icpe.macaddr, sensor.sensorid))
    message.sensor_created(sensor)
    return sensor

def Delete(sensor, icpe = None):
    if type(sensor) is str and icpe:
        sensor = SensorModel.query.join(iCPEModel).\
                filter(SensorModel.sensorid == sensor).\
                filter(iCPEModel.macaddr == icpe).first()

        if sensor is None:
            raise LookupError('Sensor not found')

    db.session.delete(sensor)
    db.session.commit()
    logger.info("Deleted Sensor {}:{}".format(icpe.macaddr, sensor.sensorid))
    return sensor

def Save(sensor):
    db.session.add(sensor)
    db.session.commit()
    sensor.redis.Load(sensor)
    return sensor

def List(icpe = None):
    if icpe is None:
        return [sensor for sensor in SensorModel.query.all()]
    if type(icpe) is str:
        icpe = iCPEModel.query.filter_by(macaddr = icpe).first()
        if icpe is None:
            raise LookupError('iCPE not found')
    return [sensor for sensor in icpe.sensors]


def Get(icpe, sensor):
    return db.session.query(SensorModel).\
            join(SensorModel.icpe).\
            filter(SensorModel.sensorid == str(sensor)).\
            filter(iCPEModel.macaddr == icpe).first()
