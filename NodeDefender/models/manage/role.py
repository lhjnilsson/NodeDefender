from ... import UserDatastore, db
from ..SQL import UserModel, UserRoleModel
from . import logger

def Init():
    UserDatastore.create_role(name='technician', description='Permission to\
                              modify Sensors on Nodes')
    UserDatastore.create_role(name='admin', description='Permission to\
                              add, modify and delete items in member Groups')
    UserDatastore.create_role(name='superuser', description='Permission to do\
                              anything avalible, on any group')
    return db.session.commit()

def technician(email):
    user = UserDatastore.get_user(email)
    if user is None:
        raise LookupError('Canot find {}'.format(email))
    role = UserDatastore.find_role('technician')
    if role is None:
        Init()
        role = UserDatastore.find_role('technician')
    UserDatastore.add_role_to_user(user, role)
    return db.session.commit()

def admin(email):
    user = UserDatastore.get_user(email)
    if user is None:
        raise LookupError('Canot find {}'.format(email))
    role = UserDatastore.find_role('admin')
    if role is None:
        Init()
        role = UserDatastore.find_role('admin')
    UserDatastore.add_role_to_user(user, role)
    technician(email)
    return db.session.commit()

def superuser(email):
    user = UserDatastore.get_user(email)
    if user is None:
        raise LookupError('Canot find {}'.format(email))
    role = UserDatastore.find_role('superuser')
    if role is None:
        Init()
        role = UserDatastore.find_role('superuser')
    UserDatastore.add_role_to_user(user, role)
    technician(email)
    admin(email)
    return db.session.commit()

def Users(role):
    if type(role) is str:
        role = UserRoleModel.query.filter_by(name = role).first()
        if role is None:
            raise LookupError('Role not found')

    return [member for member in role.users]
