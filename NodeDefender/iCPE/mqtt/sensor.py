from . import msg, Fire, mqttconn

@mqttconn
def Query(mac, sensorid, ipaddr = '127.0.0.1', port = 1883):
    return Fire(ipaddr, port, msg.format(mac, sensorid, 'info', 'qry'))
