from NodeDefender.db.sql import SQL, iCPEModel, NodeModel
import NodeDefender
from NodeDefender.db import redis, logger
from redlock import RedLock
from datetime import datetime

def get_sql(mac_address):
    return SQL.session.query(iCPEModel).filter(mac_address == mac_address).first()

def update_sql(mac_address, **kwargs):
    icpe = get_sql(mac_address)
    if icpe is None:
        return False

    try:
        for key, value in kwargs.items():
            if key not in icpe.columns():
                continue
            setattr(icpe, key, value)
    except ValueError:
        print("Wrong Data: ", kwargs)

    SQL.session.add(icpe)
    SQL.session.commit()
    return icpe

def create_sql(mac_address, mqttsrc):
    if get_sql(mac_address):
        return False
    mqtt = NodeDefender.db.mqtt.get(**mqttsrc)
    icpe = iCPEModel(mac_address)
    mqtt.icpes.append(icpe)
    SQL.session.add(mqtt, icpe)
    SQL.session.commit()
    logger.info("Created SQL Entry for {!r}".format(mac_address))
    return icpe

def delete_sql(mac_address):
    icpe = get_sql(mac_address)
    if icpe is None:
        return False
    SQL.session.delete(icpe)
    logger.info("Deleted SQL Entry for {!r}".format(mac_address))
    return SQL.session.commit()

def get_redis(mac_address):
    return redis.icpe.get(mac_address)

def update_redis(mac_address, **kwargs):
    return redis.icpe.save(mac_address, **kwargs)

def delete_redis(mac_address):
    return redis.icpe.flush(mac_address)

def get(mac_address):
    icpe = get_redis(mac_address)
    if len(icpe):
        return icpe
    if redis.icpe.load(get_sql(mac_address)):
        logger.debug('Loaded iCPE: {!r}'.format(mac_address))
        return get_redis(mac_address)
    return False

def create(mac_address, mqttsrc):
    if not create_sql(mac_address, mqttsrc):
        return False
    NodeDefender.mqtt.command.icpe.zwave_info(mac_address)
    NodeDefender.mqtt.command.icpe.system_info(mac_address)
    return get_redis(mac_address)

def update(mac_address, **data):
    update_sql(mac_address, **data)
    return update_redis(mac_address, **data)

def delete(mac_address):
    for sensor in NodeDefender.db.sensor.list(mac_address):
        NodeDefender.db.sensor.delete(mac_address, sensor.sensor_id)
        
    delete_sql(mac_address)
    delete_redis(mac_address)
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
        cached = get(icpe.mac_address)
        if not cached:
            continue
        if float(cached['lastUpdated']) - current_time > 1200:
            mark_offline(cached)
        NodeDefender.mqtt.command.icpe.zwave_info(icpe.mac_address)
        NodeDefender.mqtt.command.icpe.system_info(icpe.mac_address)
    return True

def unassigned(user):
    return SQL.session.query(iCPEModel).\
            filter(iCPEModel.node == None).all()

def sensors(mac_address):
    sensors = redis.sensor.list(mac_address)
    if len(sensors):
        return sensors
    if load_redis(mac_address):
        return redis.sensor.list(mac_address)
    return False

def update_state(mac_address, state):
    icpe = get(mac_address)
    if not icpe:
        return False
    icpe['state'] = state
    websocket.icpe.state(mac_address, state)
    update_redis(icpe)
    return True

def connection(mac_address):
    icpe = get(mac_address)
    if not icpe:
        return False
    return {'ipAddress' : icpe['ipAddress']}

def power(mac_address):
    icpe = get(mac_address)
    if not icpe:
        return False
    return {'power' : icpe['power']}
