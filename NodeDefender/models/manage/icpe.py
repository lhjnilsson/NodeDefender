from ..SQL import iCPEModel, NodeModel, MQTTModel
from ... import db
from . import logger

def List():
    return [icpe for icpe in iCPEModel.query.all()]

def Get(icpe):
    return iCPEModel.query.filter_by(macaddr = icpe).first()

def Create(mac, node = None, ipaddr = None, port = None):
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
    return icpe

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
