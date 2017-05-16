from ..SQL import MessageModel
from ... import db

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
    db.sesion.add(icpe)
    db.session.commit()
    return True

def sensor_created(sensor):
    subject = "Sensor Created"
    body = _sensor_created_template.foramt(sensor.name,
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
