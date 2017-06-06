from . import redisconn
from ... import celery
from datetime import datetime
from .decorators import LookupCommandclass
'''
Common Format
    {
    commandclass
    cmdname
    last_updated
    ... Dynamic per Commandclass
    }

'''
@LookupCommandclass
@redisconn
def Load(commandclass, conn):
    if not commandclass:
        return None
    if not commandclass.supported:
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
def Get(mac, sensorid, commandclass, conn):
    return conn.hgetall(mac + sensorid + commandclass)

@redisconn
def Fields(mac, sensorid, commandclass, conn):
    fieldlist = conn.smembers(mac + sensorid + commandclass + ':fields')
    return [field for field in fieldlist]

@redisconn
def Save(mac, sensorid, cmd, conn, **kwargs):
    for key, value in kwargs.items():
        conn.hmset(mac + sensorid + cmd, {key : value})
    conn.hmset(mac + sensorid + cmd, {'last_updated' : str(datetime.now())})
    return True
