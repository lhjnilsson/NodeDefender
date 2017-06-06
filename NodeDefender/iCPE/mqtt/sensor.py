from . import msg, Fire, mqttconn

@mqttconn
def Query(mac, sensorid, host = '127.0.0.1', port = 1883):
    return Fire(host, port, msg.format(mac, sensorid, 'info', 'qry'))

@mqttconn
def Sup(mac, sensorid, commandclass, host = '127.0.0.1', port = 1883):
    return Fire(host, port, msg.format(mac, sensorid, commandclass+':sup', 'get'))
