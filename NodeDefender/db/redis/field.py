from datetime import datetime
import NodeDefender
from NodeDefender.db.redis import redisconn

@redisconn
def load(commandclass, conn, **kwargs):
    if commandclass is None:
        return None
    kwargs['icpe'] = commandclass.sensor.icpe.macaddr
    kwargs['sensor'] = commandclass.sensor.sensorid
    kwargs['commandclass'] = commandclass.name
    kwargs['value'] = None
    kwargs['lastUpdated'] = datetime.now().timestamp()
    kwargs['loadedAt'] = datetime.now().timestamp()
    conn.sadd(commandclass.sensor.icpe.macaddr +\
              commandclass.sensor.sensorid +':fields', kwargs['name'])
    conn.hmset(commandclass.sensor.icpe.macaddr +\
               commandclass.sensor.sensorid + kwargs['name'], kwargs)
    return kwargs

@redisconn
def save(macaddr, sensorid, name, conn, **kwargs):
    field  = conn.hgetall(macaddr + sensorid + name)
    for key, value in kwargs.items():
        field[key] = str(value)
    field['lastUpdated'] = datetime.now().timestamp()
    NodeDefender.db.redis.icpe.updated(macaddr)
    NodeDefender.db.redis.sensor.updated(macaddr, sensorid)
    return conn.hmset(macaddr + sensorid + name, field)

@redisconn
def list(macaddr, sensorid, conn):
    return conn.smembers(macaddr + sensorid + ":fields")

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
