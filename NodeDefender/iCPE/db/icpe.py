from . import redisconn
from ...models.manage import icpe as iCPESQL
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
def Create(mac):
    if iCPESQL.Get(mac):
        raise ValueError('Already exists')
    return iCPESQL.Create(mac)

@redisconn
def Load(mac, conn):
    icpe = iCPESQL.Get(mac)
    if icpe is None:
        return None

    i = {
        'alias' : icpe.alias,
        'mac' : icpe.mac,
        'ipaddr' : icpe.ipaddr,
        'online' : False,
        'battery' : None,
        'loaded_at' : datetime.now(),
        'last_online' : False
    }
    conn.hmset(mac, i)
    return i

@redisconn
def Save(mac, conn, **kwargs):
    icpe = conn.hmgetall(mac)
    for key, value in kwargs:
        icpe[key] = value

    conn.hmset(mac, icpe)
    return icpe

def CreateLoadQuery(mqtt, mac, sensorid):
    if Load(mac, sensorid) is not None:
        raise ValueError('Already exists')
    
    Create(mac)
    Load(mac)
    mqtt.icpe.Query(mac, mqtt)
    return True
