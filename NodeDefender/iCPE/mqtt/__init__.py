from paho.mqtt import client as mqttcl
from collections import namedtuple
from ...models.manage import mqtt as MQTTSQL
from ...models.manage import icpe as iCPESQL
from functools import wraps

msg = 'icpe/0x{}/cmd/node/{}/class/{}/act/{}'

def mqttconn(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'host' not in kwargs:
            host, port = iCPESQL.MQTT(args[0])
            return func(*args, host = host, port = port)
        return func(*args, **kwargs)
    return wrapper

def Fire(host, port, topic, payload = None):
    client = mqttcl.Client()
    try:
        client.connect(host, port)
    except TimeoutError:
        Check(host, port)
        return False

    client.publish(topic, payload)
    return True

def Check(host, port):
    mqtt = MQTTSQL.Get(host, port)
    if mqtt is None:
        raise LookupError('MQTT not found')

    client = mqttcl.Client()
    try:
        client.connect(host, port)
        mqtt.online = True
    except TimeoutError:
        mqtt.online = False

    return MQTTSQL.Save(mqtt)

from . import sensor, icpe, zwave
