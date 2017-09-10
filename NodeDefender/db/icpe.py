from NodeDefender.db.sql import SQL, iCPEModel, NodeModel
import NodeDefender
from NodeDefender.db import redis, logger
from redlock import RedLock
from datetime import datetime

def get_sql(macaddr):
    return SQL.session.query(iCPEModel).filter(macaddr == macaddr).first()

def update_sql(macaddr, **kwargs):
    icpe = get_sql(macaddr)
    if icpe is None:
        return False

    for key, value in kwargs:
        if key not in icpe.columns():
            continue
        setattr(icpe, key, value)

    SQL.session.add(icpe)
    SQL.session.comit()
    return icpe

def create_sql(macaddr, mqttsrc):
    if get_sql(macaddr):
        return False
    mqtt = NodeDefender.db.mqtt.get(**mqttsrc)
    icpe = iCPEModel(macaddr)
    mqtt.icpes.append(icpe)
    SQL.session.add(mqtt, icpe)
    SQL.session.commit()
    logger.info("Created SQL Entry for {!r}".format(macaddr))
    return icpe

def delete_sql(macaddr):
    icpe = get_sql(macaddr)
    if icpe is None:
        return False
    SQL.session.delete(icpe)
    logger.info("Deleted SQL Entry for {!r}".format(macaddr))
    return SQL.session.commit()

def get_redis(macaddr):
    return redis.icpe.get(macaddr)

def update_redis(macaddr, **kwargs):
    return redis.icpe.save(macaddr, **kwargs)

def delete_redis(macaddr):
    return redis.icpe.flush(macaddr)

def get(macaddr):
    icpe = get_redis(macaddr)
    if len(icpe):
        return icpe
    if redis.icpe.load(get_sql(macaddr)):
        logger.debug('Loaded iCPE: {!r}'.format(macaddr))
        return get_redis(macaddr)
    return False

def create(macaddr, mqttsrc):
    if not create_sql(macaddr, mqttsrc):
        return False
    NodeDefender.mqtt.command.icpe.zwave.info.qry(macaddr)
    NodeDefender.mqtt.command.icpe.zwave.node.list(macaddr)
    return get_redis(macaddr)

def update(macaddr, **data):
    return update_redis(macaddr, **data)

def delete(macaddr):
    for sensor in NodeDefender.db.sensor.list(macaddr):
        NodeDefender.db.sensor.delete(macaddr, sensor.sensorid)
        
    delete_sql(macaddr)
    delete_redis(macaddr)
    return True

def list(node = None):
    if node:
        return  SQL.session.query(iCPEModel).join(iCPEModel.node).\
                filter(NodeModel.name == node).all()
    return SQL.session.query(iCPEModel).all()

def load(node = None):
    icpes = list(node)
    current_time = datetime.now().timestamp()
    for icpe in icpes:
        cached = get(icpe.macaddr)
        if not cached:
            continue
        if float(cached['lastUpdated']) - current_time > 1200:
            mark_offline(cached)
        NodeDefender.mqtt.command.icpe.zwave.info.qry(icpe.macaddr)
        NodeDefender.mqtt.command.icpe.zwave.node.list(icpe.macaddr)

def unassigned(user):
    return SQL.session.query(iCPEModel).\
            filter(iCPEModel.node == None).all()

def sensors(macaddr):
    sensors = redis.sensor.list(macaddr)
    if len(sensors):
        return sensors
    if load_redis(macaddr):
        return redis.sensor.list(macaddr)
    return False

def update_state(macaddr, state):
    icpe = get(macaddr)
    if not icpe:
        return False
    icpe['state'] = state
    websocket.icpe.state(macaddr, state)
    update_redis(icpe)
    return True

def connection(macaddr):
    icpe = get(macaddr)
    if not icpe:
        return False
    return {'ipAddress' : icpe['ipAddress']}

def power(macaddr):
    icpe = get(macaddr)
    if not icpe:
        return False
    return {'power' : icpe['power']}
