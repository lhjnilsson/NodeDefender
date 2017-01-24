from ... import UserDatastore, db
from ..SQL import UserModel, UserRoleModel
from . import logger

def Create(name, description):
    role = UserRoleModel.query.filter_by(name = name).first()
    if role is not None:
        raise ValueError('Role already exists')

    UserDatastore.create_role(name=name, description=description)
    db.session.commit()
    logger.info("Created Role: {}".format(name))
    return True

def Delete(name):
    if type(name) is str:
        try:
            index = int(name)
            role = UserRoleModel.query.filter_by(id = index).first()
        except ValueError:
            role = UserRoleModel.query.filter_by(name = name).first()

    if role is None:
        return LookupError('Unable to find NOde')
    
    db.session.delete(role)
    db.session.commit()
    logger.info("Deleted Role: {}".format(role.name))
    return role

def Get(name):
    if type(name) is str:
        try:
            index = int(name)
            role = UserRoleModel.query.filter_by(id = index).first()
        except ValueError:
            role = UserRoleModel.query.filter_by(name = name).first()

    return role

def List():
    return [role for role in UserRoleModel.query.all()]

def Users(role):
    if type(role) is str:
        role = UserRoleModel.query.filter_by(name = role).first()
        if role is None:
            raise LookupError('Role not found')

    return [member for member in role.users]
