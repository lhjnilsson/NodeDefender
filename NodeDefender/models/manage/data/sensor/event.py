from datetime import datetime, timedelta
from ....SQL import EventModel
from ... import icpe as iCPESQL
from ... import sensor as SensorSQL
from ... import cmdclass as CmdclassSQL


def Latest(node):
    return EventModel.query.filter_by(name = node).first()

def Get(icpe, sensor, from_date = (datetime.now() - timedelta(days=7)), to_date =
        datetime.now()):
    return session.query(EventModel).filter(name == node, date > from_date, date
                                            < to_date)

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
