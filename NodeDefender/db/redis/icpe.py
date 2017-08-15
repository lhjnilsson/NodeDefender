from NodeDefender.db.redis import redisconn
from datetime import datetime

@redisconn
def load(icpe, conn):
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

    return conn.hmset(icpe.macaddr, i)

@redisconn
def get(mac, conn):
    return conn.hgetall(mac)

@redisconn
def save(mac, conn, **kwargs):
    icpe = conn.hgetall(mac)
    for key, value in kwargs.items():
        icpe[key] = value
    return conn.hmset(mac, icpe)

@redisconn
def list(node, conn):
    return conn.smembers(node + ":icpes")

@redisconn
def flush(macaddr, conn):
    if conn.hkeys(macaddr):
        return conn.hdel(macaddr, *conn.hkeys(macaddr))
    else:
        return True
