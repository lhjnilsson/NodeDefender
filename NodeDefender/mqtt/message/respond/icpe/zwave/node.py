import NodeDefender

def list(topic, payload):
    return NodeDefender.db.sensor.verify_list(topic['macAddress'], payload)
