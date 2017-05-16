from ..SQL import iCPEModel, NodeModel, MQTTModel
from ... import db
from . import logger
from redlock import RedLock
from ..manage import message

def List():
    return [icpe for icpe in iCPEModel.query.all()]

def Unassigned(user = None):
    return [icpe for icpe in iCPEModel.query.filter_by(node = None)]

def Get(icpe):
    return iCPEModel.query.filter_by(macaddr = icpe).first()

def MQTT(macaddr):
    icpe = iCPEModel.query.filter_by(macaddr = macaddr).first()
    return icpe.mqtt[0].ipaddr, icpe.mqtt[0].port

def Create(mac, node = None, ipaddr = None, port = None):
    print(mac)
    lock = RedLock(mac)
    if lock.acquire() is False:
        return False

    if Get(mac) is not None:
        raise ValueError('iCPE Already exists')

    icpe = iCPEModel(mac)

    if ipaddr:
        if type(ipaddr) is str:
            mqtt = MQTTModel.query.filter_by(ipaddr = ipaddr).first()
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

def Enable(icpe, ipaddr = None, port = None):
    icpe = Get(icpe)
    icpe.enabled = True
    if ipaddr and port:
        ipaddr = str(ipaddr)
        port = int(port)
        mqtt = MQTTModel.query.filter_by(ipaddr = ipaddr, port = port).first()
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
