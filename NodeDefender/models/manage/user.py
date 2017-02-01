from ... import UserDatastore, db
from flask_security import utils
from flask_script import Command, prompt, prompt_pass
from ..SQL import UserModel, GroupModel
from . import logger

def Create(name, password = None):
    if UserDatastore.get_user(name):
        raise ValueError('User already present')
    if password:
        encrypted_password = utils.encrypt_password(password)
        user = UserDatastore.create_user(email=name, password=encrypted_password)
    else:
        user = UserDatastore.create_user(email=name, password=None)
    db.session.commit()
    logger.info("Created user: {}".format(user.email))
    return user

def Delete(email):
    user = UserModel.query.filter_by(email = email).first()
    if user is None:
        raise LookupError('Cant find user')
    UserDatastore.delete_user(user)
    db.session.commit()
    logger.info("Deleted user: {}".format(user.email))
    return user

def Get(email):
    return UserModel.query.filter_by(email = user).first()

def List():
    return [user for user in UserModel.query.all()]

def Friends(user):
    user = UserModel.query.filter_by(email=user).first()
    if user is None:
        raise KeyError('User does not exists')
    
    if user.has_role('superuser'):
        return List()

    groupnames = [g.name for g in user.group] 
    return UserModel.query.filter(UserModel.group.any(GroupModel.name.in_(groupnames)))

def Groups(user):
    if type(user) is str:
        user = UserModel.query.filter_by(email = user).first()
        if user is None:
            raise LookupError('User not found')

    return [group for group in user.group]

def Join(email, groupname):
    user = UserDatastore.get_user(email)
    if user is None:
        raise LookupError('Cant find User')

    group = GroupModel.query.filter_by(name = groupname).first()
    if group is None:
        raise LookupError('Cant find Group')

    group.users.append(user)
    db.session.add(group)
    db.session.commit()
    logger.info("User {} Joined Group {}".format(user.email, group.name))
    return user

def Leave(email, groupname):
    user = UserDatastore.get_user(email)
    if user is None:
        raise LookupError('Cant find User')

    group = GroupModel.query.filter_by(name = groupname).first()
    if group is None:
        raise LookupError('Cant find Group')

    group.users.remove(user)
    db.session.add(user)
    db.session.commit()
    logger.info("User {} Left Group {}".format(user.email, group.name))
    return user

def Roles(user):
    if type(user) is str:
        user = UserModel.query.filter_by(email = user).first()
        if user is None:
            raise LookupError('User not found')
    
    return [role for role in user.roles]

def Add(user, role):
    if type(user) is str:
        user = UserDatastore.get_user(user)
        if user is None:
            raise LookupError('Cant find User')

    if type(role) is str:
        role = UserDatastore.find_role(role)
        if role is None:
            raise LookupError('Cant find Role')

    UserDatastore.add_role_to_user(user, role)
    db.session.commit()
    logger.info("Added Role {} to User {}".format(role.name, user.email))
    return user

def Remove(user, role):
    if type(user) is str:
        user = UserDatastore.get_user(user)
        if user is None:
            raise LookupError('Cant find User')

    if type(role) is str:
        role = UserDatastore.find_role(role)
        if role is None:
            raise LookupError('Cant find Role')

    UserDatastore.remove_role_from_user(user, role)
    db.session.commit()
    logger.info("Removed Role {} from User {}".format(role.name, user.email))
    return user
