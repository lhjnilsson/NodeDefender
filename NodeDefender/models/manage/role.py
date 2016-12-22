from ... import UserDatastore, db
from flask_script import Command, prompt, prompt_pass
from ..SQL import UserModel, UserRoleModel

def Add(user, role):
    if type(user) is str:
        user = UserModel.query.filter_by(email = user).first()
        if user is None:
            raise LookupError('User not found')

    if type(role) is str:
        role = UserRoleModel.query.filter_by(name = role).first()
        if role is None:
            raise LookupError('Role not found')

    UserDatastore.add_role_to_user(user, role)
    db.session.commit()
    return role

def Remove(user, role):
    if type(user) is str:
        user = UserModel.query.filter_by(email = user).first()
        if user is None:
            raise LookupError('User not found')

    if type(role) is str:
        role = UserRoleModel.query.filter_by(name = role).first()
        if role is None:
            raise LookupError('Role not found')

    role.members.delete(user)
    db.session.add(role)
    db.session.commit()
    return role

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
