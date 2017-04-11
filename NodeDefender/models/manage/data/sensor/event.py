from datetime import datetime, timedelta
from ....SQL import EventModel, iCPEModel, SensorModel
from ... import icpe as iCPESQL
from ... import sensor as SensorSQL
from ... import cmdclass as CmdclassSQL


def Latest(icpe, sensor):
    return EventModel.query.join(iCPEModel).join(SensorModel).\
            filter(iCPEModel.macaddr == icpe).\
            filter(SensorModel.macaddr == sensor).first()

def Get(icpe, sensor, from_date = (datetime.now() - timedelta(days=7)), to_date =
        datetime.now()):
    return EventModel.query.join(iCPEModel).join(SensorModel).\
            filter(EventModel.date > from_date).\
            filter(EventModel.date < to_date).\
            filter(iCPEModel.macaddr == icpe).\
            filter(SensorModel.sensorid == sensor).all()

def Put(icpe, sensor, cmdclass, classtype, value):
    icpe = iCPESQL.Get(icpe)
    sensor = SensorSQL.Get(icpe.macaddr, sensor)
    cmdclass = CmdclassSQL.Get(icpe.macaddr, sensor.sensorid, cmdclass)
    event = EventModel(classtype, value)
    icpe.events.append(event)
    sensor.events.append(event)
    cmdclass.events.append(event)
    db.session.add(icpe, sensor, cmdclass)
    db.session.commit()
