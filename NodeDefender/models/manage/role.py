from ... import UserDatastore, db
from ..SQL import UserModel, UserRoleModel

def Create(role, description):
    if type(role) is str:
        role = UserRoleModel.query.filter_by(name = role).first()
        if role is not None:
            raise DuplicateError('Role not found')
    
    UserDatastore.create_role(name=name, description=description)
    db.session.commit()

def Delete(role):
    if type(role) is str:
        role = UserRoleModel.query.filter_by(name = role).first()
        if role is None:
            raise LookupError('Role not found')
    
    db.session.delete(role)
    db.session.commit()
    return role

def List():
    return [role for role in UserRoleModel.query.all()]

def Members(role):
    if type(role) is str:
        role = UserRoleModel.query.filter_by(name = role).first()
        if role is None:
            raise LookupError('Role not found')

    return [member for member in role.members]
