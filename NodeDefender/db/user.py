from NodeDefender.db.sql import SQL, UserModel

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
    SQL.session.save(user)
    SQL.session.commit()
    return user

def create_sql(mail):
    if get_sql(mail):
        return get_sql(mail)
    user = UserModel(mail)
    SQL.session.save(user)
    SQL.session.commit()
    return user

def delete_sql(mail):
    if not get_sql(mail):
        return False
    SQL.session.delete(get_sql(mail))
    SQL.session.commit()
    return True

def get(mail):
    return sql_sql(mail)

def list(groupName = None):
    if not groupName:
        return [user.to_json() for user in UserModel.query.all()]
    return [user.to_json() for user in \
            db.session.query(UserModel).join(UserModel.group).\
            filter(GroupModel.name == groupName).all()]

def create(mail):
    return create_sql(mail)

def delete(mail):
    return delete_sql(mail)
