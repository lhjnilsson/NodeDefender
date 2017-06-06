from . import msg, Fire, mqttconn

@mqttconn
def Set(macaddr, sensorid, commandclass, value, host = None, port = None):
    return Fire(host, port, msg.format(macaddr, sensorid, commandclass, 'set'),
                value)
