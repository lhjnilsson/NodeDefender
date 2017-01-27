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

conninfo = namedtuple('conninfo', 'ipaddr, port')

connections = set()

def Add(ip, port = 8883, username = None, password = None):
    current = List(ip)
    if current:
        if current.port == port:
            raise TypeError('Already Exisisting Connecton')
            return

    mqtt = _MQTT(ip, port)
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
        Add(m.ipaddr, m.port, m.username, m.password)

    return len(mqttlist)


class _MQTT:
    '''
    MQTT Service,
    Start a thread listening for both incoming from MQTT Broker and also an
    internal Queue. Puts Messages from broker another internal queue
    '''
    def __init__(self, ip, port):
        self.ip = ip
        self.port = int(port)
        self.online = False
        self.client = PahoMQTT.Client()
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        try:
            self.client.connect(self.ip, self.port, 60)
            self.info = {'ipaddr' : self.ip, 'port' : self.port}
            self.online = True
            self.client.loop_start()
        except ConnectionRefusedError:
            pass #log this later

    def __call__(self):
        if self.online:
            return str(self.ip) + ':' + str(self.port)
        else:
            return False

    def publish(self, event):
        self.client.publish(event)

    def on_connect(self, client, userdata, flags, rc):
        client.subscribe('icpe/#')

    def on_message(self, client, userdata, msg):
        MQTTEvent.apply_async(args=[self.info,
                                    msg.topic, msg.payload.decode('utf-8')])
