from ..SQL import GroupModel, NodeModel, LocationModel, iCPEModel
from geopy.geocoders import Nominatim
from collections import namedtuple
from ... import db

location = namedtuple('location', 'street city latitude longitude')

def Location(street, city):
    geo = Nominatim()
    coord = geo.geocode(city + ' ' + street, timeout = 10)
    if coord is None:
        raise LookupError('Cant find location')
    return location(street, city, coord.latitude, coord.longitude)

def Create(name, location):
    node = NodeModel(name, LocationModel(*location))
    db.session.add(node)
    db.session.commit()
    return node

def Delete(node):
    node = NodeModel.query.filter_by(name = node).first()
    if node is None:
        raise LookupError('Cant find node')
    
    db.session.delete(node)
    db.session.commit()
    return node

def Join(node, group):
    node = NodeModel.query.filter_by(name = node).first()
    if node is None:
        raise LookupError('Cant find node')

    group = GroupModel.query.filter_by(name = group).first()
    if group is None:
        raise LookupError('Cant find group')

    group.nodes.append(node)
    db.session.add(group)
    db.session.commit()
    return node

def Leave(node, group):
    node = NodeModel.query.filter_by(alias = node).first()
    if node is None:
        raise LookupError('Cant find node')

    group = GroupModel.query.filter_by(name = group).first()
    if group is None:
        raise LookupError('Cant find group')

    group.nodes.remove(node)
    db.session.add(node)
    db.session.commit()
    return node

def Get(name = None, mac = None):
    if name:
        return NodeModel.query.filter_by(name = node).first()
    else:
        return iCPEModel.query.filter_by(mac = mac).first().node

def List(user = None):
    if user:
        return [node for node in NodeModel.query.all()]
    return [node for node in NodeModel.query.all()]

'''
def Groups(node):
    node = NodeModel.query.filter_by(name = node).first()
    if node is None:
        raise LookupError('Cant find node')

    return [group for group in group.nodes]
'''

def iCPE(node):
    node = NodeModel.query.filter_by(name = node).first()
    if node is None:
        raise LookupError('Cant fine node')
    if node.icpe is None:
        raise LookupError('iCPE not initialized')

    return node.icpe
