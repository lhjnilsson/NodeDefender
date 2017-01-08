from .import msg, Fire, mqttconn
from ...models.manage import mqtt as MQTTSQL

@mqttconn
def SensorList(mac, mqtt):
    return Fire(mqtt.ipaddr, mqtt.port, msg.format(mac, '0', 'node', 'list'))

@mqttconn
def Network(mac, mqtt):
    return Fire(mqtt.ipaddr, mqtt.port, msg.format(mac, 'sys', 'net', 'info'))

@mqttconn
def Normal(mac, mqtt):
    return Fire(mqtt.ipaddr, mqtt.port, msg.format(mac, '0', 'mode', 'normal'))

@mqttconn
def Include(mac, mqtt):
    return Fire(mqtt.ipaddr, mqtt.port, msg.format(mac, '0', 'mode', 'include'))

@mqttconn
def Exclude(mac, mqtt):
    return Fire(mqtt.ipaddr, mqtt.port, msg.format(mac, '0', 'mode', 'exclude'))

@mqttconn
def Query(mac, mqtt):
    if not SensorList(mac, mqtt):
        return False
    if not Network(mac, mqtt):
        return False
    return True
