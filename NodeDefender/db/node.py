from NodeDefender.db.sql import SQL, GroupModel, NodeModel, LocationModel, UserModel
import NodeDefender
from geopy.geocoders import Nominatim

def get_sql(name):
    return NodeModel.query.filter_by(name = name).first()

def update_sql(name, **kwargs):
    node = get_sql(name)
    if node is None:
        return False
    for key, value in kwargs:
        if key not in node.columns():
            continue
        setattr(node, key, value)
    SQL.session.add(node)
    SQL.session.commit()
    return node

def create_sql(name):
    if get_sql(name):
        return get_sql(name)
    node = NodeModel(name)
    SQL.session.add(node)
    SQL.session.commit()
    return node

def save_sql(node):
    SQL.session.add(node)
    return SQL.session.commit()

def delete_sql(name):
    if not get_sql(name):
        return False
    SQL.session.delete(get_sql(name))
    SQL.session.commit()
    return True

def get(name):
    return get_sql(name)

def list(*groups):
    return SQL.session.query(NodeModel).join(NodeModel.groups).\
            filter(GroupModel.name.in_(groups)).all()

def create(name):
    return create_sql(name)

def set_location(name, street, city):
    node = get_sql(name)
    if node is None:
        return False
    geo = Nominatim()
    coord = geo.geocode(street + ' ' + city, timeout = 10)
    if coord is None:
        return False
    node.location = LocationModel(street, city, coord.latitude,
                                   coord.longitude)
    SQL.session.add(node)
    SQL.session.commit()
    return node


def delete(name):
    return delete_sql(name)

def add_icpe(nodeName, icpeMac):
    node = get_sql(nodeName)
    icpe = NodeDefender.db.icpe.get_sql(icpeMac)
    if icpe is None or node is None:
        return False

    node.icpe = icpe
    SQL.session.add(node)
    SQL.session.commit()
    return node

def remove_icpe(nodeName, icpeMac):
    node = get_sql(nodeName)
    icpe = NodeDefender.db.icpe.get(icpeMAc)
    if icpe is None or node is None:
        return False

    node.icpe = None
    SQL.session.add(node)
    SQL.session.commit()
    return node
