from .import msg, Fire, mqttconn

@mqttconn
def SensorList(mac, host = '127.0.0.1', port = 1883):
    return Fire(host, port, msg.format(mac, '0', 'node', 'list'))

@mqttconn
def Network(mac, host = '127.0.0.1', port = 1883):
    return Fire(host, port, msg.format(mac, 'sys', 'net', 'info'))

@mqttconn
def Normal(mac, host = '127.0.0.1', port = 1883):
    return Fire(host, port, msg.format(mac, '0', 'mode', 'normal'))

@mqttconn
def Include(mac, host = '127.0.0.1', port = 1883):
    return Fire(host, port, msg.format(mac, '0', 'mode', 'include'))

@mqttconn
def Exclude(mac, host = '127.0.0.1', port = 1883):
    return Fire(host, port, msg.format(mac, '0', 'mode', 'exclude'))

@mqttconn
def Query(mac, host = '127.0.0.1', port = 1883):
    if not SensorList(mac, host = host, port = port):
        return False
    if not Network(mac, host = host, port = port):
        return False
    return True
