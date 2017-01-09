from .import msg, Fire, mqttconn

@mqttconn
def SensorList(mac, ipaddr = '127.0.0.1', port = 1883):
    return Fire(ipaddr, port, msg.format(mac, '0', 'node', 'list'))

@mqttconn
def Network(mac, ipaddr = '127.0.0.1', port = 1883):
    return Fire(ipaddr, port, msg.format(mac, 'sys', 'net', 'info'))

@mqttconn
def Normal(mac, ipaddr = '127.0.0.1', port = 1883):
    return Fire(ipaddr, port, msg.format(mac, '0', 'mode', 'normal'))

@mqttconn
def Include(mac, ipaddr = '127.0.0.1', port = 1883):
    return Fire(ipaddr, port, msg.format(mac, '0', 'mode', 'include'))

@mqttconn
def Exclude(mac, ipaddr = '127.0.0.1', port = 1883):
    return Fire(ipaddr, port, msg.format(mac, '0', 'mode', 'exclude'))

@mqttconn
def Query(mac, ipaddr = '127.0.0.1', port = 1883):
    if not SensorList(mac, ipaddr, port):
        return False
    if not Network(mac, mqtt):
        return False
    return True
