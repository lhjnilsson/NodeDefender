from NodeDefender.db.sql import SQL, iCPEModel, SensorModel
from NodeDefender.db import redis
from NodeDefender import db, mqtt

def get_redis(macaddr, sensorid):
    return redis.sensor.get(macaddr, sensorid)

def update_redis(macaddr, sensorid, **kwargs):
    return redis.sensor.save(macaddr, sensorid, **kwargs)

def delete_redis(macaddr, sensorid):
    return redis.sensor.flush(macaddr, sensorid)

def get(macaddr, sensorid):
    sensor = get_redis(macaddr, sensorid)
    if len(sensor):
        return sensor
    if load_redis(get_sql(macaddr, sensorid)):
        return get_redis(macaddr, sensorid)
    return False

def update(macaddr, sensorid, **kwargs):
    update_sql(macaddr, sensorid, **kwargs)
    update_redis(macaddr, sensorid, **kwargs)
    return True

def list(macaddr):
    sensors = redis.sensor.list(macaddr)
    if len(sensors):
        return sensors
    if len(db.icpe.get_sql(macaddr).sensors):
        for sensor in db.icpe.get_sql(macaddr).sensors:
            redis.sensor.load(sensor)
        return redis.sensor.list(macaddr)
    return []

def create(macaddr, sensorid):
    if not create_sql(macaddr, sensorid):
        return False
    mqtt.command.zwave.info.qry(macaddr, sensorid)
    return get_redis(macaddr, sensorid)

def delete(macaddr, sensor):
    delete_redis(macaddr, sensor)
    return True

def verify_list(macaddr, sensorList):
    knownSensors = list(macaddr)
    for sensor in sensorList.split(','):
        if sensor not in knownSensors:
            create(macaddr, sensor)

    for sensor in knownSensors:
        if sensor not in sensorList:
            delete(macaddr, sensor)

    return True
