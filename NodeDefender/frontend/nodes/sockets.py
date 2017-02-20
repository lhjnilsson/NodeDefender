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
from ...iCPE.event import Socket
from ...models.redis import cmdclass as CmdclassRedis
from ...models.redis import field as FieldRedis
from ...models.redis import sensor as SensorRedis

@socketio.on('event', namespace='/nodedata')
def icpeevent(msg):
    print('EVENT')
    print(msg)
    return True
    
    SocketEvent.delay(**msg)
    if icpe.SocketEvent(**msg):
        return True
    else:
        return False

@socketio.on('SensorGet', namespace='/nodedata')
def SensorGet(msg):
    f = {}
    sensor = SensorRedis.Get(msg['macaddr'], msg['sensorid'])
    fields = SensorRedis.Fields(msg['macaddr'], msg['sensorid'])
    for field in fields:
        f[field] = FieldRedis.Get(msg['macaddr'], msg['sensorid'],
                                              field)
    
    emit('SensorRespond', (sensor, f))
    return True

@socketio.on('CmdclassGet', namespace='/nodedata')
def CmdclassGet(sensor):
    rsp = CmdclassRedis.Get(sensor['macaddr'], sensor['sensorid'], sensor['classname'])
    fields = CmdclassRedis.Fields(sensor['macaddr'], sensor['sensorid'],
                                  sensor['classname'])
    emit('CmdclassRespond', {'rsp' : rsp, 'fields' : fields})
    return True
