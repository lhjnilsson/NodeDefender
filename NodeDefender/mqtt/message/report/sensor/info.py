import NodeDefender

def qry(topic, payload):
    return NodeDefender.icpe.sensor.\
            sensor_info(topic['macAddress'], topic['node'], **payload)

def sup(topic, payload):
    if type(payload) is not dict:
        return True
    return NodeDefender.icpe.sensor.\
            commandclass_types(topic['macAddress'], topic['node'],
                               topic['commandClass'], **payload)

def evtsup(topic, payload):
    return True # Add support later
