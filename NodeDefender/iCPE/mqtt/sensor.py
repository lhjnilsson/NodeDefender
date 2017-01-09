from . import msg, Fire, mqttconn

@mqttconn
def Query(mqtt, mac, sensorid):
    return Fire(mqtt.ipaddr, mqtt.port, msg.format(mac, sensorid, 'node', 'qry'))
