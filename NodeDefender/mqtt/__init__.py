import paho.mqtt.client as PahoMQTT
from threading import Thread
from redlock import RedLock
import NodeDefender.mqtt.message

connections = []

def add_connection(host, port = 8883, username = None, password = None):
    current = List(host)
    if current:
        if current.port == port:
            raise TypeError('Already Exisisting Connecton')
            return

    mqtt = _MQTT()
    mqtt.host = host
    mqtt.port = port
    mqtt.connect()
    mqtt.loop_start()
    connections.append(mqtt)
    return True

def delete_connection(ip, port):
    pass

def list_connections(ip = None):
    if ip:
        connection = [connection for connection in connections\
                      if connection.ip == ip]
        if connection:
            return connection
        else:
            return False

    return [connection for connection in connections]

def load_connections(mqttlist = None):
    if mqttlist is None:
        mqttlist = MQTTSQL.List()

    for m in mqttlist:
        Thread(target = Add, args=[m.host, m.port, m.username,
                                   m.password]).start()
    return len(mqttlist)

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
            return str(self.ip) + ':' + str(self.port)
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
        message.event.apply_async(args=[msg.topic, msg.payload.decode('utf-8'),
                                    self.info])

@celery.task
def CheckMQTT():
    for mqtt in MQTTSQL.List():
        lock = RedLock(str(mqtt.host) + str(mqtt.port))
        if lock.acquire() is False:
            #Someone is already holding this
            continue
        m = _MQTT()
        m.host = mqtt.host
        m.port = mqtt.port
        m.username = mqtt.username
        m.password = mqtt.password
        m.connect()
        print('Going in as MQTT Handler')
        m.loop_start()
