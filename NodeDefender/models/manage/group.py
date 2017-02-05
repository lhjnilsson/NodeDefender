from ... import db
from ...models.SQL import GroupModel, UserModel
from . import logger
from . import user as UserSQL

def Create(name, description = None):
    group = GroupModel.query.filter_by(name=name).first()
    if group is not None:
        raise ValueError('Group already present')

    group = GroupModel(name, description)
    db.session.add(group)
    db.session.commit()
    logger.info("Created Group: {}".format(group.name))
    return group

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

def List():
    return [group for group in GroupModel.query.all()]
    
def Members(group):
    group = GroupModel.query.filter_by(name = groupname).first()
    return [member for member in group.members]

def Nodes(group):
    group = GroupModel.query.filter_by(name = group).first()
    return [node for node in group.nodes]


