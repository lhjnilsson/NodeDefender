import NodeDefender.mqtt.command.sensor.info
from NodeDefender.mqtt.command import topic_format, fire

def set(mac_address, sensor_id, commandclass, endpoint = None, payload = None):
    if endpoint:
        node = sensor_id + ':' + endpoint
    else:
        node = sensor_id
    topic = topic_format.format(mac_address, node, commandclass, 'set')
    print("MAC: ", mac_address)
    return fire(topic, payload = payload, icpe = mac_address)

def sensor_info(mac_address, sensor_id):
    NodeDefender.mqtt.command.sensor.info.qry(mac_address, sensor_id)
    return True
