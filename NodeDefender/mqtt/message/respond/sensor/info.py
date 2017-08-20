from NodeDefender import db

def qry(topic, payload):
    db.commandclass.verify_list(topic['macAddress'], topic['node'],\
                                payload['clslist_0'])
    data = payload
    data.pop('clslist_0')
    return db.sensor.update(topic['macAddress'], topic['node'], **data)


def sup(topic, payload):
    return db.commandclass.add_types(topic['macAddress'], topic['node'],
                              topic['commandClass'], payload['typelist'])

def evtsup(topic, payload):
    return True # Add support later
