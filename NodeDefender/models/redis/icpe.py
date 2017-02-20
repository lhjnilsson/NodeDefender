from . import redisconn
from ...models.manage import icpe as iCPESQL
from ... import celery
from datetime import datetime
from .decorators import LookupiCPE

'''
Common Format

    For iCPE:
        {
        MAC
        IP Address
        Online
        Battery
        Loaded At
        Last Online
        }
'''
@LookupiCPE
@redisconn
def Load(icpe, conn):
    if icpe is None:
        return None
    i = {
        'name' : icpe.name,
        'mac' : icpe.macaddr,
        'ipaddr' : icpe.ipaddr,
        'online' : False,
        'battery' : None,
        'loaded_at' : str(datetime.now()),
        'last_online' : False
    }

    conn.sadd(icpe.macaddr + ":sensors", [sensor.sensorid for sensor in icpe.sensors])
    return conn.hmset(icpe.macaddr, i)

@redisconn
def Get(mac, conn):
    return conn.hgetall(mac)

@redisconn
def Save(mac, conn, **kwargs):
    icpe = conn.hgetall(mac)
    for key, value in kwargs:
        icpe[key] = value
        
    return conn.hmset(mac, icpe)

@redisconn
def Sensors(mac, conn):
    return conn.smembers(mac + ":sensors")
