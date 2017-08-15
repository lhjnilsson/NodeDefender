from NodeDefender.db.redis import redisconn
from datetime import datetime

@redisconn
def load(sensor, conn):
    if sensor is None:
        return None
    s = {
        'name' : sensor.name,
        'sensorId' : sensor.sensorid,
        'vendorId' : sensor.vendor_id,
        'productType' : sensor.product_type,
        'productId' : sensor.product_id,
        'vendorName' : sensor.vendor_name,
        'productName' : sensor.product_name,
        'genericClass' : sensor.generic_class,
        'specificClass' : sensor.specific_class,
        'sleepable' : sensor.sleepable,
        'wakeup_interval' : sensor.wakeup_interval
    }
    conn.sadd(sensor.icpe.macaddr + ':sensors', sensor.sensorid)
    return conn.hmset(sensor.icpe.macaddr + sensor.sensorid, s)

@redisconn
def get(macaddr, sensorid, conn):
    return conn.hgetall(macaddr + sensorid)

@redisconn
def save(macaddr, sensorid, conn, **kwargs):
    sensor = conn.hgetall(macaddr + sensorid)
    for key, value in kwargs.items():
        sensor[key] = value
    return conn.hmset(macaddr + sensorid, sensor)

@redisconn
def list(macaddr, conn):
    return conn.smembers(macaddr + ':sensors')

@redisconn
def flush(macaddr, sensorid, conn):
    if conn.hkeys(macaddr + sensorid):
        conn.srem(macaddr + ':sensors', sensorid)
        return conn.hdel(macaddr + sensorid, *conn.hkeys(macaddr + sensorid))
    else:
        return True
