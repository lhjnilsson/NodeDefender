from ... import db
from ..SQL import MQTTModel
from . import logger

def Create(ipaddr, port, username = None, password = None):
    mqtt = MQTTModel.query.filter_by(ipaddr = ipaddr).first()
    if mqtt and int(mqtt.port) is int(port):
        raise ValueError('IP Address and Port combination already exists')

    mqtt = MQTTModel(ipaddr, port, username, password)
    db.session.add(mqtt)
    db.session.commit()
    logger.info("Created MQTT: {}:{}".format(ipaddr, str(port)))
    return mqtt

def Delete(ipaddr, port = None):
    mqtt = MQTTModel.query.filter_by(ipaddr = ipaddr).first()
    if mqtt is None:
        raise LookupError('MQTT Connection does not exist')
    
    db.session.delete(mqtt)
    db.session.commit()
    logger.info("Delted MQTT: {}:{}".format(ipaddr, str(port)))
    return mqtt

def Include(ipaddr, mac):
    mqtt = MQTTModel.query.filter_by(ipaddr = ipaddr).first()
    if mqtt is None:
        raise LookupError('MQTT Connection does not exist')

    icpe = iCPEModel.query.filter_by(macaddr = mac).first()
    if icpe is None:
        raise LookupError('iCPE not found')

    mqtt.icpes.append(icpe)
    db.session.add(mqtt)
    db.session.commit()
    logger.info("Included iCPE {} to MQTT {}:{}".format(icpe.macaddr, mqtt.ipaddr,
                                                        str(mqtt.port)))
    return mqtt

def Exclude(ipaddr, mac):
    mqtt = MQTTModel.query.filter_by(ipaddr = ipaddr).first()
    if mqtt is None:
        raise LookupError('MQTT Connection does not exist')

    icpe = iCPEModel.query.filter_by(macaddr = mac).first()
    if icpe is None:
        raise LookupError('iCPE not found')

    mqtt.icpes.remove(icpe)
    db.session.add(mqtt)
    db.session.commit()
    logger.info("Removed iCPE {} from MQTT {}:{}".fomrat(icpe.macaddr, mqtt.ipaddr,
                                                         str(mqtt.port)))
    return mqtt

def Query(ipaddr, mac):
    pass


def List():
    return [mqtt for mqtt in MQTTModel.query.all()]

def Get(ipaddr, port):
    return MQTTModel.query.first()
