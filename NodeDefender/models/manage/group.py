from ... import db
from ...models.SQL import GroupModel, UserModel, LocationModel
from . import logger
from . import user as UserSQL
from . import node as NodeSQL
from ..manage import message
from geopy.geocoders import Nominatim

def Create(name, mail = None, description = None):
    group = GroupModel.query.filter_by(name=name).first()
    if group is not None:
        raise ValueError('Group already present')

    group = GroupModel(name, mail, description)
    db.session.add(group)
    db.session.commit()
    message.group_created(group)
    logger.info("Created Group: {}".format(group.name))
    return group

def Location(group, street, city):
    if type(group) == str:
        group = Get(group)
    geo = Nominatim()
    coord = geo.geocode(city + ' ' + street, timeout = 10)
    if coord is None:
        raise LookupError('Cant find location')
    group.location = LocationModel(street, city, coord.latitude,
                                   coord.longitude)
    db.session.add(group)
    db.session.commit()
    return True

def Delete(group):
    group = GroupModel.query.filter_by(name=group).first()
    if group is None:
        raise ValueError('Group already present')

    db.session.delete(group)
    db.session.commit()
    logger.info("Deleted Group: {}".format(group.name))
    return group

def Get(group):
    return GroupModel.query.filter_by(name=group).first()

def Save(group):
    db.session.add(group)
    return db.session.commit()

def List(user = None, node = None):
    if user is None and node is None:
        return [group for group in GroupModel.query.all()]
    if user:
        user = UserSQL.Get(user)
        return [group for group in user.groups]
    if node:
        node = NodeSQL.Get(name = node)
        return [group for group in node.groups]

def Members(group):
    group = GroupModel.query.filter_by(name = groupname).first()
    return [member for member in group.members]

def Nodes(group):
    group = GroupModel.query.filter_by(name = group).first()
    return [node for node in group.nodes]


