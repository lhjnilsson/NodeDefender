from . import pool
from ...models.manage import icpe as iCPESQL
from redis import StrictRedis

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

def Load(mac):
    icpe = iCPESQL.Get(mac)
    if icpe is None:
        return None

    conn = StrictRedis(connection_pool=pool)
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

def Save(mac, **kwargs):
    conn = StrictRedis(connection_pool=pool)
    i = conn.hmgetall(mac)
    for key, value in kwargs:
        i[key] = value

    conn.hmset(mac, i)
    return i
