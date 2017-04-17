from flask_socketio import emit, send, disconnect, join_room, leave_room, \
        close_room, rooms
from ... import socketio
from ...models.manage import data as DataSQL

@socketio.on('groupEventList', namespace='/data')
def group_events(msg):
    events = DataSQL.group.event.Get(msg['group'], msg['length'])
    if events:
        emit('groupEventList', (events))
    return True

@socketio.on('icpeEventList', namespace='/data')
def icpe_events(msg):
    events = DataSQL.icpe.event.Get(msg['iCPE'], msg['length'])
    if events:
        emit('icpeEventList', (events))
    return True

@socketio.on('sensorEventList', namespace='/data')
def sensor_events(msg):
    events = DataSQL.sensor.event.Get(msg['iCPE'], msg['sensor'])
    if events:
        emit('sensorEventList', (events))
    return True

@socketio.on('groupPowerList', namespace='/data')
def group_power(msg):
    power = DataSQL.group.power.Get(msg['group'])
    if power:
        emit('groupPowerList', (power))
    return True

@socketio.on('icpePowerList', namespace='/data')
def icpe_power(msg):
    power = DataSQL.icpe.power.Get(msg['icpe'])
    if power:
        emit('icpePowerList', (power))
    return True

@socketio.on('sensorPowerList', namespace='/data')
def icpe_power(msg):
    power = DataSQL.icpe.sensor.Get(msg['icpe'])
    if power:
        emit('icpePowerList', (power))
    return True


