from . import redisconn
from .. import mqtt
from ...models.manage import icpe as iCPESQL
from ... import celery
from datetime import datetime
from . import logger
'''
Common Redis Format

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

def Create(mac, ipaddr = None, port = None):
    if iCPESQL.Get(mac):
        raise ValueError('Already exists')
    return iCPESQL.Create(mac, ipaddr = ipaddr, port = port)

@redisconn
def Load(mac, conn):
    icpe = iCPESQL.Get(mac)
    if icpe is None:
        return None

    i = {
        'name' : icpe.name,
        'mac' : icpe.macaddr,
        'ipaddr' : icpe.ipaddr,
        'online' : False,
        'battery' : None,
        'loaded_at' : datetime.now(),
        'last_online' : False
    }
    conn.hmset(mac, i)
    logger.info("Loaded iCPE: {} from Event".format(mac))
    return i

@redisconn
def LoadFromObject(icpe, conn):
    i = {
        'name' : icpe.name,
        'mac' : icpe.macaddr,
        'ipaddr' : icpe.ipaddr,
        'online' : False,
        'battery' : None,
        'loaded_at' : datetime.now(),
        'last_online' : False
    }
    conn.hmset(icpe.macaddr, i)
    logger.info("Loaded iCPE: {} from Object".format(icpe.macaddr))
    return i

@redisconn
def Get(mac, conn):
    s = conn.hgetall(mac)

    if len(s):
        return s
    else:
        return None

@redisconn
def Save(mac, conn, **kwargs):
    icpe = conn.hgetall(mac)
    for key, value in kwargs:
        icpe[key] = value
        
    conn.hmset(mac, icpe)
    return icpe

def CreateLoadQuery(mqttsrc, mac):
    if Load(mac) is not None:
        raise ValueError('Already exists')

    Create(mac, **mqttsrc)
    Load(mac)
    mqtt.icpe.Query(mac, **mqttsrc)
    return True
