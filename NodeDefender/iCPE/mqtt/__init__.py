from paho.mqtt import client as mqtt
from collections import namedtuple
from ...models.manage import mqtt as MQTTSQL

msg = 'icpe/0x{}/cmd/node/{}/class/{}/act/{}'

def mqttconn(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if type(args[0]) is not conninfo:
            return func(MQTTSQL.Get(args[0]),*args, **kwargs)
        return func(*args, **kwargs)
    return wrapper


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
    mqtt = MQTTSQL.Get(address, port)
    if mqtt is None:
        raise LookupError('MQTT not found')

    client = mqtt.Client()
    try:
        client.connect(address, port)
        mqtt.online = True
    except TimeoutError:
        mqtt.online = False

    return MQTTSQL.Save(mqtt)
