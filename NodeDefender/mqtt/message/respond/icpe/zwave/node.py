import NodeDefender

def list(topic, payload):
    return NodeDefender.icpe.sensor.verify_list(topic['macAddress'], *payload)
