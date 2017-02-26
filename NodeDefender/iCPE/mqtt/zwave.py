from . import msg, Fire, mqttconn

@mqttconn
def Set(macaddr, sensorid, cmdclass, value, ipaddr = None, port = None):
    return Fire(ipaddr, port, msg.format(macaddr, sensorid, cmdclass, 'set'),
                value)
