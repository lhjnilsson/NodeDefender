from NodeDefender.db.sql import SQL, UserModel
from NodeDefender import bcrypt

def get_sql(mail):
    return UserModel.query.filter_by(mail = mail).first()

def update_sql(mail, **kwargs):
    user = get_sql(mail)
    if user is None:
        return False
    for key, value in kwargs:
        if key not in user.columns():
            continue
        setattr(user, key, value)
    SQL.session.add(user)
    SQL.session.commit()
    return user

def create_sql(mail):
    if get_sql(mail):
        return get_sql(mail)
    user = UserModel(mail)
    SQL.session.add(user)
    SQL.session.commit()
    return user

def save_sql(user):
    SQL.session.add(user)
    return SQL.session.commit()

def delete_sql(mail):
    if not get_sql(mail):
        return False
    SQL.session.delete(get_sql(mail))
    SQL.session.commit()
    return True

def get(mail):
    return get_sql(mail)

def set_password(email, raw_password):
    user = get_sql(email)
    user.password = bcrypt.generate_password_hash(password).decode('utf-8')
    return save_sql(user)

def groups(mail):
    try:
        return [group.to_json() for group in get_sql(mail).groups]
    except AttributeError:
        return []

def set_role(mail, role):
    user = get_sql(mail)
    user.set_role(role)
    SQL.session.add(user)
    SQL.session.commit()
    return user

def get_role(mail):
    return get_sql(mail).role()

def list(*group_names):
    if not groupName:
        return [user.to_json() for user in UserModel.query.all()]
    return [user.to_json() for user in \
            db.session.query(UserModel).join(UserModel.group).\
            filter(GroupModel.name == groupName).all()]

def create(mail, firstname = None, lastname = None):
    create_sql(mail)
    update_sql(mail, **{'fistname' : firstname, 'lastname' : lastname})
    return get_sql(mail)

def update(mail, **kwargs):
    return update_sql(mail, **kwargs)

def delete(mail):
    return delete_sql(mail)
