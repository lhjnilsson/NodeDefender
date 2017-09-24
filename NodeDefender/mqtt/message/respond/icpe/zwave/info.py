import NodeDefender

def qry(topic, payload):
    return NodeDefeder.icpe.event.system_status(topic['macAddress'], payload)
