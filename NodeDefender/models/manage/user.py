from ... import UserDatastore, db
from flask_security import utils
from flask_script import Command, prompt, prompt_pass
from ..SQL import UserModel

def Create(name, password):
    if UserDatastore.get_user(name):
        raise ValueError('User already present')

    encrypted_password = utils.encrypt_password(password)
    user = UserDatastore.create_user(email=name, password=encrypted_password)
    db.session.commit()
    return user

def Delete(user):
    if type(user) is str:
        user = UserModel.query.filter_by(email=user).first()
        if not user:
            raise LookupError('User not found')

    db.session.delete(user)
    db.session.commit()
    return user

def List():
    return [user for user in UserModel.query.all()]

def Groups(user):
    if type(user) is str:
        user = UserModel.query.filter_by(email = user).first()
        if user is None:
            raise LookupError('User not found')

    return [group for group in user.groups]

def Roles(user):
    if type(user) is str:
        user = UserModel.query.filter_by(email = user).first()
        if user is None:
            raise LookupError('User not found')
    
    return [role for role in user.roles]
