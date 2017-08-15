from NodeDefender.db.sql import SQL, GroupModel, UserModel

def get_sql(name):
    return GroupModel.query.filter_by(name = name).first()

def update_sql(name, **kwargs):
    group = get_sql(name)
    if group is None:
        return False
    for key, value in kwargs:
        if key not in group.columns():
            continue
        setattr(group, key, value)
    SQL.session.save(group)
    SQL.session.commit()
    return group

def create_sql(name):
    if get_sql(name):
        return get_sql(name)
    group = GroupModel(name)
    SQL.session.save(group)
    SQL.session.commit()
    return group

def delete_sql(name):
    if not get_sql(name):
        return False
    SQL.session.delete(get_sql(name))
    SQL.session.commit()
    return True

def get(name):
    return get_sql(name)

def list(userMail = None):
    if not userMail:
        return [group.to_json() for group in GroupModel.query.all()]
    
    user = db.user.get(userMail)
    if user.superuser():
        return [group.to_json() for group in GroupModel.query.all()]
    return [group.to_json() for group in \
            db.session.query(GroupModel).join(GroupModel.user).\
            filter(UserModel.mail == userMail).all()]

def create(name):
    return create_sql(name)

def delete(name):
    return delete_sql(name)

def add_user(groupName, userMail):
    group = get_sql(groupName)
    user = db.user.get(userMail)
    if user is None or group is None:
        return False

    group.users.append(user)
    SQL.session.save(group)
    SQL.session.commit()
    return group

def remove_user(groupName, userMail):
    group = get_sql(groupName)
    user = db.user.get(userMail)
    if user is None or group is None:
        return False

    group.users.remove(user)
    SQL.session.save(group)
    SQL.session.commit()
    return group

def add_node(groupName, nodeName):
    group = get_sql(groupName)
    node = db.user.get(nodeName)
    if node is None or group is None:
        return False

    group.nodes.append(node)
    SQL.session.save(group)
    SQL.session.commit()
    return group

def remove_node(groupName, nodeName):
    group = get_sql(groupName)
    node = db.node.get(nodeName)
    if node is None or group is None:
        return False

    group.nodes.remove(node)
    SQL.session.save(group)
    SQL.session.commit()
    return group
