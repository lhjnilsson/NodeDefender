from datetime import datetime, timedelta
from ....SQL import EventModel, iCPEModel, SensorModel
from ... import icpe as iCPESQL
from ... import sensor as SensorSQL
from ... import cmdclass as CmdclassSQL
from ..... import db
from ....redis import field as FieldRedis
from .....conn.websocket import FieldEvent

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
    cmdclass = CmdclassSQL.Get(icpe.macaddr, sensor.sensorid, event.cc)
    e = EventModel(event.cctype, event.ccevent, event.value)
    
    e.node = icpe.node
    e.icpe = icpe
    e.sensor = sensor
    e.sensorclass = cmdclass

    db.session.add(e)
    db.session.commit()
    FieldEvent(FieldRedis.Update(e))
