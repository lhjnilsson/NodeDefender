from ... import db
from ..SQL import MQTTModel, GroupModel
from . import logger

def Create(host, port, username = None, password = None):
    mqtt = MQTTModel.query.filter_by(host = host).first()
    if mqtt and int(mqtt.port) is int(port):
        raise ValueError('IP Address and Port combination already exists')

    mqtt = MQTTModel(host, port, username, password)
    db.session.add(mqtt)
    db.session.commit()
    logger.info("Created MQTT: {}:{}".format(host, str(port)))
    return mqtt

def Delete(host, port = None):
    mqtt = MQTTModel.query.filter_by(host = host).first()
    if mqtt is None:
        raise LookupError('MQTT Connection does not exist')
    
    db.session.delete(mqtt)
    db.session.commit()
    logger.info("Delted MQTT: {}:{}".format(host, str(port)))
    return mqtt

def Include(host, mac):
    mqtt = MQTTModel.query.filter_by(host = host).first()
    if mqtt is None:
        raise LookupError('MQTT Connection does not exist')

    icpe = iCPEModel.query.filter_by(macaddr = mac).first()
    if icpe is None:
        raise LookupError('iCPE not found')

    mqtt.icpes.append(icpe)
    db.session.add(mqtt)
    db.session.commit()
    logger.info("Included iCPE {} to MQTT {}:{}".format(icpe.macaddr, mqtt.host,
                                                        str(mqtt.port)))
    return mqtt

def Exclude(host, mac):
    mqtt = MQTTModel.query.filter_by(host = host).first()
    if mqtt is None:
        raise LookupError('MQTT Connection does not exist')

    icpe = iCPEModel.query.filter_by(macaddr = mac).first()
    if icpe is None:
        raise LookupError('iCPE not found')

    mqtt.icpes.remove(icpe)
    db.session.add(mqtt)
    db.session.commit()
    logger.info("Removed iCPE {} from MQTT {}:{}".fomrat(icpe.macaddr, mqtt.host,
                                                         str(mqtt.port)))
    return mqtt

def Query(host, mac):
    pass


def List(current_user = None):
    if current_user is None or current_user.superuser:
        return [mqtt for mqtt in MQTTModel.query.all()]
    else:
        groups = [group.name for group in current_user.groups]
        return db.session.query(MQTTModel).join(MQTTModel.groups).\
                filter(GroupModel.name.in_(groups)).all()

def iCPE(macaddr):
    pass

def Get(host, port):
    return MQTTModel.query.filter_by(host = host, port = port).first()

def Save(model):
    db.session.add(model)
    db.session.commit()
    return True
