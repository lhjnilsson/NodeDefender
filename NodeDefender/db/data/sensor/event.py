from datetime import datetime, timedelta
from NodeDefender.db.sql import SQL, EventModel, iCPEModel, SensorModel

def Latest(icpe, sensor):
    return EventModel.query.join(iCPEModel).join(SensorModel).\
            filter(iCPEModel.macaddr == icpe).\
            filter(SensorModel.macaddr == sensor).first()

def Get(icpe, sensor, limit = None):
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


def put(icpe, sensor, event):
    icpe = NodeDefender.db.icpe.get_sql(icpe)
    sensor = NodeDefender.db.sensor.get_sql(icpe.macaddr, sensor)
    commandclass = NodeDefender.db.commandclass.get_sql(icpe.macaddr, \
                                                        sensor.sensorid,\
                                                        classnumber = event.cc)
    e = EventModel(event.value)
    if event.cctype:
        commandclasstype = NodeDefender.db.commandclass.\
                get_type(icpe.macaddr, sensor.sensorid, event.cc, event.cctype)
        e.commandclasstype = commandclasstype

    e.node = icpe.node
    e.icpe = icpe
    e.sensor = sensor
    e.commandclass = commandclass

    SQL.session.add(e)
    SQL.session.commit()

    redis = FieldRedis.Update(e, event)
