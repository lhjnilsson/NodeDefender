from datetime import datetime, timedelta
from ....SQL import EventModel, iCPEModel, SensorModel
from ... import icpe as iCPESQL
from ... import sensor as SensorSQL
from ... import cmdclass as CmdclassSQL
from ..... import db

def Latest(icpe):
    return EventModel.query.join(iCPEModel).\
            filter(iCPEModel.macaddr == icpe).first()

def Get(icpe, limit = 20):
    return EventModel.query.join(iCPEModel).\
            filter(iCPEModel.macaddr == icpe).\
            order_by(EventModel.date.desc()).limit(int(limit)).all()

def Put(icpe, sensor, cmdclass, classtype, value):
    icpe = iCPESQL.Get(icpe)
    sensor = SensorSQL.Get(icpe.macaddr, sensor)
    cmdclass = CmdclassSQL.Get(icpe.macaddr, sensor.sensorid, cmdclass)
    event = EventModel(classtype, value)
    event.node = icpe.node
    event.icpe = icpe
    event.sensor = sensor
    event.sensorclass = cmdclass
    db.session.add(event)
    db.session.commit()
