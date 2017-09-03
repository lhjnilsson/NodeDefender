from NodeDefender.db.sql import SQL, GroupModel, UserModel
import NodeDefender

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
    SQL.session.add(group)
    SQL.session.commit()
    return group

def create_sql(name):
    if get_sql(name):
        return get_sql(name)
    group = GroupModel(name)
    SQL.session.add(group)
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

def list(user_mail = None):
    if not user_mail:
        return [group.to_json() for group in GroupModel.query.all()]
    
    user = NodeDefender.db.user.get(user_mail)
    if user.superuser():
        return [group.to_json() for group in GroupModel.query.all()]
    return [group.to_json() for group in user.groups]

def create(name):
    return create_sql(name)

def update(name, **kwargs):
    return update_sql(name, **kwargs)

def location(name, street, city):
    group = get_sql(name)
    if group is None:
        return False
    geo = Nominatim()
    coord = geo.geocode(street + ' ' + city, timeout = 10)
    if coord is None:
        return False
    group.location = LocationModel(street, city, coord.latitude,
                                   coord.longitude)
    SQL.session.add(group)
    SQL.session.commit()
    return group

def delete(name):
    return delete_sql(name)

def add_user(group_name, user_mail):
    group = get_sql(group_name)
    user = db.user.get(user_mail)
    if user is None or group is None:
        return False

    group.users.append(user)
    SQL.session.save(group)
    SQL.session.commit()
    return group

def remove_user(group_name, user_mail):
    group = get_sql(group_name)
    user = db.user.get(user_mail)
    if user is None or group is None:
        return False

    group.users.remove(user)
    SQL.session.save(group)
    SQL.session.commit()
    return group

def add_node(group_name, node_name):
    group = get_sql(group_name)
    node = db.user.get(node_name)
    if node is None or group is None:
        return False

    group.nodes.append(node)
    SQL.session.save(group)
    SQL.session.commit()
    return group

def remove_node(group_name, node_name):
    group = get_sql(group_name)
    node = db.node.get(node_name)
    if node is None or group is None:
        return False

    group.nodes.remove(node)
    SQL.session.save(group)
    SQL.session.commit()
    return group
