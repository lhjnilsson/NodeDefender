from NodeDefender.db.redis import redisconn
from datetime import datetime

@redisconn
def load(icpe, conn):
    if icpe is None:
        return None
    i = {
        'name' : icpe.name,
        'node' : icpe.node.name if icpe.node else "unassigned",
        'sensors' : len(icpe.sensors),
        'mqtt' : icpe.mqtt[0].host + ':' + str(icpe.mqtt[0].port),
        'macAddress' : icpe.macaddr,
        'ipaddr' : icpe.ipaddr,
        'online' : False,
        'battery' : None,
        'createdAt' : icpe.created_on.timestamp(),
        'lastUpdated' : datetime.now().timestamp(),
        'loadedAt' : datetime.now().timestamp()
    }

    return conn.hmset(icpe.macaddr, i)

@redisconn
def get(macaddr, conn):
    return conn.hgetall(macaddr)

@redisconn
def save(macaddr, conn, **kwargs):
    icpe = conn.hgetall(macaddr)
    for key, value in kwargs.items():
        icpe[key] = value
    icpe['lastUpdated'] = datetime.now().timestamp()
    return conn.hmset(macaddr, icpe)

@redisconn
def list(node, conn):
    return conn.smembers(node + ":icpes")

@redisconn
def updated(macaddr, conn):
    return conn.hmset(macaddr, {'lastUpdated' : datetime.now().timestamp()})

@redisconn
def flush(macaddr, conn):
    if conn.hkeys(macaddr):
        return conn.hdel(macaddr, *conn.hkeys(macaddr))
    else:
        return True
