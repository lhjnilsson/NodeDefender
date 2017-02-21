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
from flask_socketio import emit, send, disconnect, join_room, leave_room, \
        close_room, rooms
from ... import socketio
from ...iCPE.event import WebSocket as SocketEvent
from ...models.redis import cmdclass as CmdclassRedis
from ...models.redis import field as FieldRedis
from ...models.redis import sensor as SensorRedis

@socketio.on('ZWaveSet', namespace='/nodedata')
def icpeevent(msg):
    print(msg)
    SocketEvent(msg['macaddr'], msg['sensorid'], msg['cmdclass'], msg['value'])
    return True

@socketio.on('SensorGet', namespace='/nodedata')
def SensorGet(msg):
    fieldlist = []
    sensor = SensorRedis.Get(msg['macaddr'], msg['sensorid'])
    fields = SensorRedis.Fields(msg['macaddr'], msg['sensorid'])
    for field in fields:
        fieldlist.append(FieldRedis.Get(msg['macaddr'], msg['sensorid'],
                                              field))
    
    emit('SensorRespond', (sensor, fieldlist))
    return True
