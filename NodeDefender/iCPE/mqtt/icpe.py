from .import msg, Fire, mqttconn

@mqttconn
def SensorList(mqtt, mac):
    return Fire(mqtt.ipaddr, mqtt.port, msg.format(mac, '0', 'node', 'list'))

@mqttconn
def Network(mqtt, mac):
    return Fire(mqtt.ipaddr, mqtt.port, msg.format(mac, 'sys', 'net', 'info'))

@mqttconn
def Normal(mqtt, mac):
    return Fire(mqtt.ipaddr, mqtt.port, msg.format(mac, '0', 'mode', 'normal'))

@mqttconn
def Include(mqtt, mac):
    return Fire(mqtt.ipaddr, mqtt.port, msg.format(mac, '0', 'mode', 'include'))

@mqttconn
def Exclude(mqtt, mac):
    return Fire(mqtt.ipaddr, mqtt.port, msg.format(mac, '0', 'mode', 'exclude'))

@mqttconn
def Query(mqtt, mac):
    if not SensorList(mac, mqtt):
        return False
    if not Network(mac, mqtt):
        return False
    return True
