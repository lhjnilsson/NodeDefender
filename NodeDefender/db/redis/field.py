from datetime import datetime
from NodeDefender.db.redis import redisconn

@redisconn
def load(sensor, conn, **kwargs):
    if field is None:
        return None
    kwargs['icpe'] = sensor.icpe.macaddr
    kwargs['sensor'] = sensor.sensorid
    kwargs['value'] = None
    kwargs['last_updated'] = None,
    kwargs['loaded_at'] = str(datetime.now())
    conn.sadd(sensor.icpe.macaddr + sensor.sensorid +':fields', kwargs['name'])
    conn.hmset(sensor.icpe.macaddr + sensor.sensorid + field['name'], kwargs)
    return kwargs

@redisconn
def save(macaddr, sensorid, name, conn, **kwargs):
    field  = conn.hgetall(macaddr + sensorid + name)
    for key, value in kwargs.items():
        field[key] = value
    return conn.hmset(macaddr + sensorid + name)

@redisconn
def get(macaddr, sensorid, name, conn):
    return conn.hgetall(macaddr + sensorid + name)

@redisconn
def flush(macaddr, sensorid, name, conn):
    if conn.hkeys(macaddr+ sensorid + name):
        conn.srem(macaddr + sensorid + ':fields', name)
        return conn.hdel(macaddr + sensorid + name, \
                         *conn.hkeys(macaddr+ sensorid + name))
    else:
        return True
