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
from ...models.manage import icpe as iCPESQL
from ...models.manage import sensor as SensorSQL
from ...models.redis import sensor as SensorRedis
from ...models.redis import field as FieldRedis
from ... import iCPE

@socketio.on('list', namespace='/sensor')
def List(msg):
    icpes = [sensor.to_json() for sensor in SensorSQLSQL.List(msg['icpe'])]
    return True

@socketio.on('info', namespace='/sensor')
def Info(msg):
    sensor = SensorSQL.Get(msg['icpe'], msg['sensor'])
    if sensor:
        emit('info', (sensor.to_json()))
    return True

@socketio.on('update', namespace='/sensor')
def update_fields(sensor):
    iCPE.db.sensor.Update(sensor['icpe'], sensor['sensor'])
    return True

@socketio.on('updateConfig', namespace='/sensor')
def update_config(icpe, sensorid, name):
    sensor = SensorSQL.Get(icpe, sensorid)
    if sensor is None:
        emit('error', 'Sensor not found', namespace='/general')
        return False
    sensor.name = name
    SensorSQL.Save(sensor)
    emit('reload', namespace='/general')
    return True

@socketio.on('fields', namespace='/sensor')
def fields(icpe, sensor):
    fields = []
    for field in SensorRedis.Fields(icpe, sensor):
        fields.append(FieldRedis.Get(icpe, sensor, field))

    emit('fields', fields)
    return True
