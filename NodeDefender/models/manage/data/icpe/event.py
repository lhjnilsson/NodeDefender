from datetime import datetime, timedelta
from ....SQL import EventModel, iCPEModel, SensorModel
from ... import icpe as iCPESQL
from ... import sensor as SensorSQL
from ... import commandclass as CommandclassSQL
from ..... import db

def Latest(icpe):
    return EventModel.query.join(iCPEModel).\
            filter(iCPEModel.macaddr == icpe).first()

def Get(icpe, limit = 20):
    return EventModel.query.join(iCPEModel).\
            filter(iCPEModel.macaddr == icpe).\
            order_by(EventModel.date.desc()).limit(int(limit)).all()

def Put(icpe, sensor, commandclass, classtype, value):
    icpe = iCPESQL.Get(icpe)
    sensor = SensorSQL.Get(icpe.macaddr, sensor)
    commandclass = CommandclassSQL.Get(icpe.macaddr, sensor.sensorid, commandclass)
    event = EventModel(classtype, value)
    event.node = icpe.node
    event.icpe = icpe
    event.sensor = sensor
    event.sensorclass = commandclass
    db.session.add(event)
    db.session.commit()
