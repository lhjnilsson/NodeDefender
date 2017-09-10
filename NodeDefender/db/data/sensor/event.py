from datetime import datetime, timedelta
from NodeDefender.db.sql import SQL, EventModel, iCPEModel, SensorModel
import NodeDefender

def latest(icpe, sensor):
    return EventModel.query.join(iCPEModel).join(SensorModel).\
            filter(iCPEModel.macaddr == icpe).\
            filter(SensorModel.macaddr == sensor).first()

def get(icpe, sensor, limit = None):
    if limit is None:
        limit = 10
    return SQL.session.query(EventModel).\
            join(EventModel.sensor).\
            join(EventModel.icpe).\
            filter(iCPEModel.macaddr == icpe).\
            filter(SensorModel.sensorid == sensor).\
            order_by(EventModel.date.desc()).limit(int(limit)).all()

def average(icpe, sensor, time_ago = None):
    if time_ago is None:
        time_ago = (datetime.now() - timedelta(days=1))

    total_events = SQL.session.query(EventModel).\
            join(EventModel.sensor).\
            join(EventModel.icpe).\
            filter(iCPEModel.macaddr == icpe).\
            filter(SensorModel.sensorid == sensor).\
            filter(EventModel.date > time_ago).all()

    ret_data = {}
    ret_data['icpe'] = icpe
    ret_data['sensor'] = sensor
    ret_data['total'] = len(total_events)
    ret_data['critical'] = len([event for event in total_events if
                                event.critical])
    ret_data['normal'] = len([event for event in total_events if
                              event.normal])
    return ret_data


def put(mac, sensorid, commandclass, commandclasstype, state, value):
    icpe = NodeDefender.db.icpe.get_sql(mac)
    sensor = NodeDefender.db.sensor.get_sql(mac, sensorid)
    commandclass = NodeDefender.db.commandclass.\
            get_sql(mac, sensorid, classname = commandclass)
    
    if commandclass is None:
        return 

    event = EventModel(state, value)

    event.node = icpe.node
    event.icpe = icpe
    event.sensor = sensor
    event.commandclass = commandclass

    if commandclasstype:
        event.commandclasstype = NodeDefender.db.commandclass.\
                get_type(mac, sensorid, commandclass.name, commandclasstype)
    SQL.session.add(event)
    SQL.session.commit()
    return True
