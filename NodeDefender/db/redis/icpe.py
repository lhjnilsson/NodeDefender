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
        'mac_address' : icpe.macaddr,
        'ip_address' : icpe.ip_address,
        'ip_dhcp' : icpe.ip_dhcp,
        'ip_gateway' : icpe.ip_gateway,
        'ip_subnet' : icpe.ip_subnet,
        'online' : False,
        'battery' : None,
        'date_created' : icpe.created_on.timestamp(),
        'date_updated' : datetime.now().timestamp(),
        'date_loaded' : datetime.now().timestamp()
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
    icpe['date_updated'] = datetime.now().timestamp()
    return conn.hmset(macaddr, icpe)

@redisconn
def list(node, conn):
    return conn.smembers(node + ":icpes")

@redisconn
def updated(macaddr, conn):
    return conn.hmset(macaddr, {'date_updated' : datetime.now().timestamp()})

@redisconn
def flush(macaddr, conn):
    if conn.hkeys(macaddr):
        return conn.hdel(macaddr, *conn.hkeys(macaddr))
    else:
        return True
