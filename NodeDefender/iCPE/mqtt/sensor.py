from . import msg, Fire, mqttconn

@mqttconn
def Query(ipaddr, port, mac, sensorid):
    return Fire(ipaddr, port, msg.format(mac, sensorid, 'node', 'qry'))
