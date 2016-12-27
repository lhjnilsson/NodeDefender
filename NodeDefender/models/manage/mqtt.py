from ... import db
from ..SQL import MQTTModel

def Create(ipaddr, port, username = None, password = None):
    mqtt = MQTTModel.query.filter_by(ipaddr = ipaddr).first()
    if mqtt and int(mqtt.port) is int(port):
        raise ValueError('IP Address and Port combination already exists')

    mqtt = MQTTModel(ipaddr, port, username, password)
    db.session.add(mqtt)
    db.session.commit()
    return mqtt

def Delete(ipaddr, port = None):
    mqtt = MQTTModel.query.filter_by(ipadd = ipaddr).first()
    if mqtt is None:
        raise LookupError('MQTT Connection does not exist')
    
    db.session.delete(mqtt)
    db.session.commit()
    return mqtt

def List():
    return [mqtt for mqtt in MQTTModel.query.all()]

def Get(ipaddr):
    return MQTTModel.query.filter_by(ipaddr = ipaddr).first()
