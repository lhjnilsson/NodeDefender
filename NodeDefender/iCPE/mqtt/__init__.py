from paho.mqtt import client as mqtt

msg = 'icpe/0x{}/cmd/node/{}/class/{}/act/{}'


def Fire(address, port, topic, payload = None):
    client = mqtt.Client()
    try:
        client.connect(address, port, timeout)
    except TimeoutError:
        Check(address, port)
        return False

    client.publish(topic, paylod)
    return True

def Check(address, port):
    m = MQTTSQL.Get(address, port)
    if m is None:
        raise LookupError('MQTT not found')

    client = mqtt.Client()
    try:
        client.connect(address, port)
        m.online = True
    except TimeoutError:
        m.online = False

    return MQTTSQL.Save(m)
