from NodeDefender.db.redis import redisconn
import NodeDefender
from datetime import datetime

@redisconn
def load(sensor, conn):
    if sensor is None:
        return None
    s = {
        'name' : sensor.name,
        'icpe' : sensor.icpe.macaddr,
        'sensor_id' : sensor.sensorid,
        'vendor_id' : sensor.vendor_id,
        'product_type' : sensor.product_type,
        'product_id' : sensor.product_id,
        'vendor_name' : sensor.vendor_name,
        'product_name' : sensor.product_name,
        'device_type' : sensor.device_type,
        'library_type' : sensor.library_type,
        'sleepable' : sensor.sleepable,
        'wakeup_interval' : sensor.wakeup_interval,
        'date_updated' : datetime.now().timestamp(),
        'date_created' : sensor.date_created.timestamp(),
        'date_loaded' : datetime.now().timestamp()
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
    sensor['date_updated'] = datetime.now().timestamp()
    NodeDefender.db.redis.icpe.updated(macaddr)
    return conn.hmset(macaddr + sensorid, sensor)

@redisconn
def list(macaddr, conn):
    return conn.smembers(macaddr + ':sensors')

@redisconn
def updated(macaddr, sensorid, conn):
    return conn.hmset(macaddr + sensorid, {'date_updated' : \
                                           datetime.now().timestamp()})

@redisconn
def flush(macaddr, sensorid, conn):
    if conn.hkeys(macaddr + sensorid):
        conn.srem(macaddr + ':sensors', sensorid)
        return conn.hdel(macaddr + sensorid, *conn.hkeys(macaddr + sensorid))
    else:
        return True
