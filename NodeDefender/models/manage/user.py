from ... import db, bcrypt
from flask_script import Command, prompt, prompt_pass
from ..SQL import UserModel, GroupModel
from . import logger

def Create(email):
    if UserModel.query.filter_by(email = email).first():
        raise ValueError('User already exists')
    user = UserModel(email)
    db.session.add(user)
    db.session.commit()
    logger.info("Created user: {}".format(user.email))
    return user

def Password(email, password):
    user = Get(email)
    user.password = bcrypt.generate_password_hash(password).decode('utf-8')
    db.session.add(user)
    db.session.commit()

def Delete(email):
    user = UserModel.query.filter_by(email = email).first()
    if user is None:
        raise LookupError('Cant find user')
    db.session.delete(user)
    db.session.commit()
    logger.info("Deleted user: {}".format(user.email))
    return user

def Enable(user):
    user = Get(user)
    user.active = True
    db.session.add(user)
    db.session.commit()
    return user

def Lock(user):
    user = Get(user)
    user.active = False
    db.session.add(user)
    db.session.commit()
    return user

def Get(email):
    return UserModel.query.filter_by(email = email).first()

def List():
    return [user for user in UserModel.query.all()]

def Save(user):
    db.session.add(user)
    return db.session.commit()

def Friends(user):
    user = UserModel.query.filter_by(email=user).first()
    if user is None:
        raise KeyError('User does not exists')
    
    if user.has_role('superuser'):
        return List()

    groupnames = [g.name for g in user.groups] 
    return UserModel.query.filter(UserModel.group.any(GroupModel.name.in_(groupnames)))

def Groups(user):
    if type(user) is str:
        user = UserModel.query.filter_by(email = user).first()
        if user is None:
            raise LookupError('User not found')

    return [group for group in user.groups]

def Join(email, groupname):
    user = UserModel.query.filter_by(email = email).first()
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
    user = UserModel.query.filter_by(email = email).first()
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

def Role(user):
    return role.Role(user)

