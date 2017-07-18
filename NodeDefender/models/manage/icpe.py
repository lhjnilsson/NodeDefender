from ..SQL import iCPEModel, NodeModel, MQTTModel
from ... import db
from . import logger
from redlock import RedLock
from ..manage import message

def get_sql(macaddr):
    return iCPEModel.query.filter_by(macaddr = macaddr).first()

def get_redis(macaddr):
    return conn.hgetall(macaddr)

def update_sql(macaddr, **kwargs):
    icpe = get_sql(macaddr)
    if icpe is None:
        return False

    for key, value in kwargs:
        if key not in icpe.columns():
            continue
        setattr(icpe, key, value)

    db.session.save(icpe)
    db.session.comit()
    return icpe

def update_redis(macaddr, **kwargs):
    icpe = get_redis(macaddr)
    if not len(icpe) and not load_redis(macaddr):
        return False

    for key, value in kwargs:
        icpe[key] = value

    return conn.hmset(macaddr, icpe)

def load_redis(macaddr):
    icpe = get_sql(macaddr)
    if icpe is None:
        return False
    model = {'name' : icpe.name,
             'macaddr' : icpe.macaddr,
             'ipaddr' : icpe.network.ipaddr,
             'online' : False,
             'battery' : None,
             'loaded_at' : str(datetime.now()),
             'last_onlnie' : False}
    conn.hmset(macaddr, model)
    con.sadd(macaddr + ':sensors', [sensor.sensorid for sensor in
                                    icpe.sensors])
    return get_redis(macaddr)

def delete_sql(macaddr):
    icpe = get_sql(macaddr)
    db.session.delete(icpe)
    return db.session.commit()

def delete_redis(macaddr):
    conn.delete(macaddr)

def get(macaddr):
    icpe = get_redis(macaddr)
    if len(icpe):
        return icpe
    if load_redis(macaddr):
        return get_redis(macaddr)
    return False

def list(node):
    nodes = db.session.query(iCPEModel).join(iCPEModel.node).\
            filter(NodeModel.name == node).all()
    return [node.name for node in nodes]

def sensors(macaddr):
    sensors = conn.smembers(macaddr + ":sensors")
    if len(sensors):
        return sensors
    if load_redis(macaddr):
        return conn.smembers(macaddr + ":sensors")
    return False

def state(macaddr, state):
    icpe = get(macaddr)
    if not icpe:
        return False
    icpe['state'] = state
    websocket.icpe.state(macaddr, state)
    update_redis(icpe)
    return True

#####---###

def List():
    return [icpe for icpe in iCPEModel.query.all()]

def Unassigned(user = None):
    return [icpe for icpe in iCPEModel.query.filter_by(node = None)]

def Get(icpe):
    return iCPEModel.query.filter_by(macaddr = icpe).first()

def MQTT(macaddr):
    icpe = iCPEModel.query.filter_by(macaddr = macaddr).first()
    return icpe.mqtt[0].host, icpe.mqtt[0].port

def Create(mac, node = None, host = None, port = None):
    print(mac)
    lock = RedLock(mac)
    if lock.acquire() is False:
        return False

    if Get(mac) is not None:
        raise ValueError('iCPE Already exists')

    icpe = iCPEModel(mac)

    if host:
        if type(host) is str:
            mqtt = MQTTModel.query.filter_by(host = host).first()
            if mqtt is None:
                raise LookupError('MQTT not found')
        mqtt.icpes.append(icpe)
        db.session.add(mqtt)
    
    if node:
        if type(node) is str:
            node = NodeModel.query.filter_by(name = Node).first()
            if node is None:
                raise LookupError('Node not found')
        node.icpes.append(icpe)
        db.session.add(node)


    db.session.add(icpe)
    db.session.commit()
    logger.info("Added iCPE: {}".format(icpe.macaddr))
    lock.release()
    message.icpe_created(icpe)
    return icpe

def Enable(icpe, host = None, port = None):
    icpe = Get(icpe)
    icpe.enabled = True
    if host and port:
        host = str(host)
        port = int(port)
        mqtt = MQTTModel.query.filter_by(host = host, port = port).first()
        icpe.mqtt.append(mqtt)

    db.session.add(icpe)
    db.session.commit()
    return True

def Disable(icpe):
    icpe = Get(icpe)
    icpe.enabled = False
    db.session.add(icpe)
    db.session.commit()
    return True

def Enabled(icpe):
    icpe = Get(icpe)
    return icpe.enabled


def Delete(icpe):
    if type(icpe) is str:
        icpe = iCPEModel.query.filter_by(macaddr = icpe).first()

    db.session.delete(icpe)
    db.session.commit()
    logger.info("Deleted iCPE: {}".format(icpe.macaddr))
    return True

def Join(icpe, node):
    if type(icpe) is str:
        icpe = iCPEModel.query.filter_by(macaddr = icpe).first()
        if icpe is None:
            raise LookupError('iCPE not found')

    if type(node) is str:
        node = NodeModel.query.filter_by(name = node).first()
        if node is None:
            raise LookupError('Node not found')

    node.icpe = icpe
    db.session.add(node)
    db.session.commit()
    logger.info("Added iCPE: {} to Node: {}".format(icpe.macaddr, node.name))

def Leave(icpe, node):
    if type(icpe) is str:
        icpe = iCPEModel.query.filter_by(macaddr = icpe).first()
        if icpe is None:
            raise LookupError('iCPE not found')

    if type(group) is str:
        group = GroupModel.query.filter_by(name = group).first()
        if group is None:
            raise LookupError('Group not found')

    group.icpes.remove(icpe)
    db.session.add(group)
    db.session.commit()
    logger.info("Removed iCPE: {} from Node: {}".format(icpe.macaddr, node.name))
