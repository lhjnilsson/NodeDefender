import NodeDefender

def qry(topic, payload):
    NodeDefender.db.commandclass.\
            verify_list(topic['macAddress'], topic['node'],\
                        payload['clslist_0'])
    data = payload
    data.pop('clslist_0')
    return NodeDefender.db.sensor.\
            update(topic['macAddress'], topic['node'], **data)

def sup(topic, payload):
    if type(payload) is not dict:
        return True
    return NodeDefender.db.commandclass.\
            add_types(topic['macAddress'], topic['node'],\
                      topic['commandClass'], payload['typelist'])

def evtsup(topic, payload):
    return True # Add support later
