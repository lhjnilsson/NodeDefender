import paho.mqtt.client as PahoMQTT
from threading import Thread
from NodeDefender.mqtt import logger, message
import NodeDefender

def add(host, port = 8883, username = None, password = None):
    if NodeDefender.db.mqtt.online(host, port):
        return
    mqtt = _MQTT()
    mqtt.host = host
    mqtt.port = port
    mqtt.connect()
    mqtt.loop_start()
    return True

def load(mqttlist = None):
    if mqttlist is None:
        mqttlist = NodeDefender.db.mqtt.list()

    for m in mqttlist:
        Thread(target=add, args=[m.host, m.port]).start()
    return len(mqttlist)

def connection(host, port):
    client = PahoMQTT.Client()
    client.connect(host, port, 60)
    return client

class _MQTT:
    '''
    MQTT Service,
    Start a thread listening for both incoming from MQTT Broker and also an
    internal Queue. Puts Messages from broker another internal queue
    '''
    def __init__(self):
        self.host = None
        self.port = None
        self.username = None
        self.password = None
        self.client = PahoMQTT.Client()
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
       
    def __call__(self):
        if self.online:
            return str(self.host) + ':' + str(self.port)
        else:
            return False

    def loop_start(self):
        if self.host is None:
            raise AttributeError('IP Address not set')
        if self.port is None:
            raise AttributeError('Port not set')
        self.info = {'host' : self.host, 'port' : self.port}
        self.client.loop_start()

    def connect(self):
        self.client.connect(str(self.host), int(self.port), 60)
        self.connect = True
        return True

    def on_connect(self, client, userdata, flags, rc):
        client.subscribe('icpe/#')

    def on_message(self, client, userdata, msg):
        message.event(msg.topic, msg.payload.decode('utf-8'), self.info)
        #message.event.apply_async(args=[msg.topic, msg.payload.decode('utf-8'),
        #                            self.info])
