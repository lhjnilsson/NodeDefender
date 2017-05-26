from . import msg, Fire, mqttconn

@mqttconn
def Set(macaddr, sensorid, commandclass, value, ipaddr = None, port = None):
    return Fire(ipaddr, port, msg.format(macaddr, sensorid, commandclass, 'set'),
                value)
