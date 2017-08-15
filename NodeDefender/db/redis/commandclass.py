from NodeDefender.db.redis import redisconn
from datetime import datetime

@redisconn
def load(commandclass, conn):
    if not commandclass:
        return None
    if not commandclass.classname:
        return False

    conn.sadd(commandclass.sensor.icpe.macaddr + commandclass.sensor.sensorid +\
              ":commandclasses", commandclass.name)
    return conn.hmset(commandclass.sensor.icpe.macaddr + \
                      commandclass.sensor.sensorid + \
                      commandclass.name, \
                        {
                            'number' : commandclass.number,
                            'name' : commandclass.name,
                            'last_updated' : str(datetime.now()),
                            'loaded_at' : str(datetime.now()),
                       })

@redisconn
def get(mac, sensorid, commandclass, conn):
    return conn.hgetall(mac + sensorid + commandclass)

def list(macaddr, sensorid, conn):
    return conn.smembers(macaddr + sensorid + ':commandclasses')

@redisconn
def save(mac, sensorid, cmd, conn, **kwargs):
    for key, value in kwargs.items():
        conn.hmset(mac + sensorid + cmd, {key : value})
    conn.hmset(mac + sensorid + cmd, {'last_updated' : str(datetime.now())})
    return True
