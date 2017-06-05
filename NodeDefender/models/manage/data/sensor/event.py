from datetime import datetime, timedelta
from ....SQL import EventModel, iCPEModel, SensorModel
from ... import icpe as iCPESQL
from ... import sensor as SensorSQL
from ... import commandclass as CommandclassSQL
from ... import commandclasstype as CommandclasstypeSQL
from ..... import db
from ....redis import field as FieldRedis
from .....conn.websocket import ZWaveEvent

def Latest(icpe, sensor):
    return EventModel.query.join(iCPEModel).join(SensorModel).\
            filter(iCPEModel.macaddr == icpe).\
            filter(SensorModel.macaddr == sensor).first()

def Get(icpe, sensor, limit = None):
    if limit is None:
        limit = 10
    return db.session.query(EventModel).\
            join(EventModel.sensor).\
            join(EventModel.icpe).\
            filter(iCPEModel.macaddr == icpe).\
            filter(SensorModel.sensorid == sensor).\
            order_by(EventModel.date.desc()).limit(int(limit)).all()

def Put(icpe, sensor, event):
    icpe = iCPESQL.Get(icpe)
    sensor = SensorSQL.Get(icpe.macaddr, sensor)
    commandclass = CommandclassSQL.Get(icpe.macaddr, sensor.sensorid, event.cc)
    e = EventModel(event.value)
    if event.cctype:
        commandclasstype = CommandclasstypeSQL.Get(icpe.macaddr, sensor.sensorid,
                                               event.cc, event.cctype)
        e.commandclasstype = commandclasstype

    e.node = icpe.node
    e.icpe = icpe
    e.sensor = sensor
    e.commandclass = commandclass

    db.session.add(e)
    db.session.commit()

    redis = FieldRedis.Update(e, event)

    ZWaveEvent(redis)
