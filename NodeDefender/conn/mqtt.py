'''
Copyright (c) 2016 Connection Technology Systems Northern Europe

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE
SOFTWARE.
'''
import paho.mqtt.client as PahoMQTT
from ..iCPE.event import MQTT as MQTTEvent
from collections import namedtuple
from ..models.manage import mqtt as MQTTSQL
from threading import Thread
from .. import celery
from redlock import RedLock

conninfo = namedtuple('conninfo', 'ipaddr, port')

connections = set()

def Add(ipaddr, port = 8883, username = None, password = None):
    current = List(ipaddr)
    if current:
        if current.port == port:
            raise TypeError('Already Exisisting Connecton')
            return

    mqtt = _MQTT()
    mqtt.ipaddr = ipaddr
    mqtt.port = port
    mqtt.connect()
    mqtt.loop_start()
    connections.add(mqtt)
    return True

def List(ip = None):
    if ip:
        connection = [connection for connection in connections\
                      if connection.ip == ip]
        if connection:
            return connection
        else:
            return False

    return [connection for connection in connections]

def Delete(ip, port):
    pass

def SendMessage(topic, payload, ip, port = None):
    pass

def Load(mqttlist = None):
    if mqttlist is None:
        mqttlist = MQTTSQL.List()

    for m in mqttlist:
        Thread(target = Add, args=[m.ipaddr, m.port, m.username,
                                   m.password]).start()

    return len(mqttlist)


class _MQTT:
    '''
    MQTT Service,
    Start a thread listening for both incoming from MQTT Broker and also an
    internal Queue. Puts Messages from broker another internal queue
    '''
    def __init__(self):
        self.ip = None
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
        if self.ipaddr is None:
            raise AttributeError('IP Address not set')
        if self.port is None:
            raise AttributeError('Port not set')
        self.info = {'ipaddr' : self.ipaddr, 'port' : self.port}
        self.client.loop_start()

    def connect(self):
        self.client.connect(str(self.ipaddr), int(self.port), 60)
        self.connect = True
        return True

    def on_connect(self, client, userdata, flags, rc):
        client.subscribe('icpe/#')

    def on_message(self, client, userdata, msg):
        MQTTEvent.apply_async(args=[msg.topic, msg.payload.decode('utf-8'),
                                    self.info])

@celery.task
def CheckMQTT():
    for mqtt in MQTTSQL.List():
        lock = RedLock(str(mqtt.ipaddr) + str(mqtt.port))
        if lock.acquire() is False:
            #Someone is already holding this
            continue
        m = _MQTT()
        m.ipaddr = mqtt.ipaddr
        m.port = mqtt.port
        m.username = mqtt.username
        m.password = mqtt.password
        m.connect()
        print('Going in as MQTT Handler')
        m.loop_start()
