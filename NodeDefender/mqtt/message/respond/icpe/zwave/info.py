import NodeDefender

def qry(topic, payload):
    return NodeDefeder.icpe.event.system_status(topic['mac_address'], payload)
