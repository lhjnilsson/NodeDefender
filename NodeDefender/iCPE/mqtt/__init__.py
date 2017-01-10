from paho.mqtt import client as mqttcl
from collections import namedtuple
from ...models.manage import mqtt as MQTTSQL
from functools import wraps

msg = 'icpe/0x{}/cmd/node/{}/class/{}/act/{}'

def mqttconn(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        '''
        if 'ipaddr' and 'port' not in kwargs:
            pass
            ipaddr, port = MQTTSQL.Get(args[0])
            return func(*args, ipaddr = ipaddr, port = port, **kwargs)
        '''
        return func(*args, **kwargs)
    return wrapper

def Fire(ipaddr, port, topic, payload = None):
    client = mqttcl.Client()
    try:
        client.connect(ipaddr, port)
    except TimeoutError:
        Check(ipaddr, port)
        return False

    client.publish(topic, payload)
    return True

def Check(ipaddr, port):
    mqtt = MQTTSQL.Get(ipaddr, port)
    if mqtt is None:
        raise LookupError('MQTT not found')

    client = mqttcl.Client()
    try:
        client.connect(ipaddr, port)
        mqtt.online = True
    except TimeoutError:
        mqtt.online = False

    return MQTTSQL.Save(mqtt)

from . import sensor, icpe
