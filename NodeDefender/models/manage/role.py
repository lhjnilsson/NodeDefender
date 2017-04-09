from ..SQL import UserModel
from ... import db

def AddRole(user, role):
    if type(user) is str:
        user = UserModel.query.filter_by(email = user).first()
    
    if user is None:
        raise LookupError('User not found')
    
    if role.lower() == 'observer':
        user.technician = False
        user.administrator = False
        user.superuser = False
    elif role.lower() == 'technician':
        user.technician = True
        user.administrator = False
        user.superuser = False
    elif role.lower() == 'administrator':
        user.technician = True
        user.administrator = True
        user.superuser = False
    elif role.lower() == 'superuser':
        user.technician = True
        user.administrator = True
        user.superuser = True
    else:
        raise ValueError('Not a valid Role')

    db.session.add(user)
    db.session.commit()
    return

def Role(user):
    if type(user) is str:
        user = UserModel.query.filter_by(email = user).first()
    if user is None:
        raise LookupError('User not found')

    if user.technician:
        return 'Technician'
    if user.administrator:
        return 'Administrator'
    if user.superuser:
        return 'Superuser'

    return 'None'
