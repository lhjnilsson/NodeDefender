from NodeDefender.db.sql import SQL, UserModel
from NodeDefender import bcrypt

def get_sql(email):
    return UserModel.query.filter_by(email = email).first()

def update_sql(email, **kwargs):
    user = get_sql(email)
    if user is None:
        return False
    for key, value in kwargs:
        if key not in user.columns():
            continue
        setattr(user, key, value)
    SQL.session.add(user)
    SQL.session.commit()
    return user

def create_sql(email):
    if get_sql(email):
        return get_sql(email)
    user = UserModel(email)
    SQL.session.add(user)
    SQL.session.commit()
    return user

def save_sql(user):
    SQL.session.add(user)
    return SQL.session.commit()

def delete_sql(email):
    if not get_sql(email):
        return False
    SQL.session.delete(get_sql(email))
    SQL.session.commit()
    return True

def get(email):
    return get_sql(email)

def set_password(eemail, raw_password):
    user = get_sql(eemail)
    user.password = bcrypt.generate_password_hash(password).decode('utf-8')
    return save_sql(user)

def groups(email):
    try:
        return [group.to_json() for group in get_sql(email).groups]
    except AttributeError:
        return []

def set_role(email, role):
    user = get_sql(email)
    user.set_role(role)
    SQL.session.add(user)
    SQL.session.commit()
    return user

def get_role(email):
    return get_sql(email).role()

def list(*group_names):
    if not groupName:
        return [user.to_json() for user in UserModel.query.all()]
    return [user.to_json() for user in \
            db.session.query(UserModel).join(UserModel.group).\
            filter(GroupModel.name == groupName).all()]

def create(email, firstname = None, lastname = None):
    create_sql(email)
    update_sql(email, **{'fistname' : firstname, 'lastname' : lastname})
    return get_sql(email)

def update(email, **kwargs):
    return update_sql(email, **kwargs)

def delete(email):
    return delete_sql(email)
