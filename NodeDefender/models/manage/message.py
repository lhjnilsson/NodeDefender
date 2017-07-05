from ..SQL import MessageModel, UserModel, GroupModel, NodeModel, iCPEModel,\
SensorModel
from ... import db
from sqlalchemy import or_

def messages(user, limit = 10):
    if type(user) is str:
        user = db.session.query(UserModel).filter(UserModel.email ==
                                                  user).first()
    
    if user is None:
        return False

    if user.has_role('superuser'):
        return db.session.query(MessageModel).\
                order_by(MessageModel.date.desc()).limit(int(limit)).all()
    
    groups = [group for group in user.groups]
    nodes = [node for node in [group.nodes for group in groups][0]]
    icpes = [node.icpe for node in nodes]

    # Revert from list of models to a list of string
    groups = [group.name for group in groups]
    nodes = [node.name for node in nodes]
    icpes = [icpe.macaddr for icpe in icpes]

    gq = db.session.query(MessageModel).join(MessageModel.group).\
            filter(GroupModel.name.in_(groups))
    nq = db.session.query(MessageModel).join(MessageModel.node).\
            filter(NodeModel.name.in_(nodes))
    iq = db.session.query(MessageModel).join(MessageModel.icpe).\
            filter(iCPEModel.macaddr.in_(icpes))

    return gq.union(nq).union(iq).order_by(MessageModel.date.desc()).\
            limit(int(limit)).all()

def group_messages(group, limit = 10):
    if type(group) is str:
        group = db.session.query(GroupModel).filter(GroupModel.name ==
                                                    group).first()
    if group is None:
        return False
    return group.messages

    nodes = [node for node in group.nodes]
    icpes = [node.icpe for node in nodes]
    sensors = [sensor.id for sensor in [icpe.sensors for icpe in icpes][0]]

    # Revert from list for models to a list for strings
    nodes = [node.name for node in nodes]
    icpes = [icpe.macaddr for icpe in icpes]

    return db.session.query(MessageModel).\
            join(MessageModel.group).\
            join(MessageModel.node).\
            join(MessageModel.icpe).\
            join(MessageModel.sensor).\
            filter(GroupModel.name == group.name,\
                       NodeModel.name.in_(*[nodes]),\
                       iCPEModel.macaddr.in_(*[icpes]),\
                       SensorModel.id.in_(*[sensors])\
                      ).order_by(MessageModel.date.desc()).limit(int(limit)).all()

def user_messages(user, limit = 10):
    if type(user) is str:
        user = db.session.query(UserModel).\
                filter(UserModel.email == user).first()

    if user is None:
        return False

    return db.session.query(MessageModel).\
            filter(MessageModel.user.email == user.email).\
            order_by(MessageModel.date.desc()).limit(int(limit)).all()

def node_messages(node, limit = 10):
    if type(node) is str:
        node = db.session.query(NodeModel).filter(NodeModel.name == node).first()

    if node is None:
        return False
    
    sensors = [sensor.sensorid for sensor in node.icpe.sensors]
    return db.session.query(MessageModel).\
            filter(or_(MessageModel.node == node,
                       MessageModel.sensors.sensorid.in_(*[sensors]),
                    )).order_by(MessageModel.date.desc()).limit(int(limit)).all()


def group_created(group):
    subject = "Group Created"
    body = _group_created_template.format(group.name, group.email)
    message = MessageModel(subject, body)
    group.messages.append(message)
    db.session.add(group)
    db.session.commit()
    return True

def user_created(user):
    subject = "User Created"
    body = _user_created_template.format(user.email)
    message = MessageModel(subject, body)
    user.messages.append(message)
    db.session.add(user)
    db.session.commit()
    return True

def node_created(node):
    subject = "Node Created"
    body = _node_created_template.format(node.name, node.location.street,
                                            node.location.city)
    message = MessageModel(subject, body)
    node.messages.append(message)
    db.session.add(node)
    db.session.commit()
    return True

def icpe_created(icpe):
    subject = "iCPE Created"
    body = _icpe_created_template.format(icpe.macaddr)
    message = MessageModel(subject, body)
    icpe.messages.append(message)
    db.session.add(icpe)
    db.session.commit()
    return True

def sensor_created(sensor):
    subject = "Sensor Created"
    body = _sensor_created_template.format(sensor.name,
                                              sensor.icpe.macaddr)
    message = MessageModel(subject, body)
    sensor.messages.append(message)
    db.session.add(message)
    db.session.commit()
    return True

_group_created_template = "Group {} created. Mail Address: {}."
_user_created_template = "User {} created"
_node_created_template = "Node {} created, location {}, {}."
_icpe_created_template = "iCPE {} created"
_sensor_created_template = "Sensor {} created. Connected to iCPE {}"
