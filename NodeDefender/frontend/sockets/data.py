from flask_socketio import emit, send, disconnect, join_room, leave_room, \
        close_room, rooms
from ... import socketio
from ...models.manage import data as DataSQL

# Events
@socketio.on('groupEventGet', namespace='/data')
def group_events(msg):
    events = DataSQL.group.event.Get(msg['group'], msg['length'])
    if events:
        emit('groupEventGet', (events))
    return True

@socketio.on('icpeEventGet', namespace='/data')
def icpe_events(msg):
    events = DataSQL.icpe.event.Get(msg['iCPE'], msg['length'])
    if events:
        emit('icpeEventGet', (events))
    return True

@socketio.on('sensorEventGet', namespace='/data')
def sensor_events(msg):
    events = DataSQL.sensor.event.Get(msg['iCPE'], msg['sensor'])
    if events:
        emit('sensorEventGet', (events))
    return True

# Power
@socketion.on('powerAverage', namespace='/data')
def power_average(msg):
    pass

# Heat
@socketio.on('groupHeatLatest', namespace='/data')
def group_heat_latest(msg):
    heat = DataSQL.group.heat.Latest(msg['group'])
    if heat:
        emit('groupHeatLatest', (heat))
    return True

@socketio.on('icpeHeatLatest', namespace='/data')
def icpe_heat_latest(msg):
    heat = DataSQL.icpe.heat.Latest(msg['icpe'])
    if heat:
        emit('icpeHeatLatest', (heat))
    return True

@socketio.on('sensorHeatLatest', namespace='/data')
def sensor_heat_latest(msg):
    heat = DataSQL.sensor.heat.Latest(msg['icpe'], msg['sensor'])
    if heat:
        emit('sensorHeatLatest', (heat))
    return True

@socketio.on('groupHeatGet', namespace='/data')
def group_heat_get(msg):
    heat = DataSQL.group.heat.Get(msg['group'])
    if heat:
        emit('groupHeatGet', (heat))
    return True

@socketio.on('icpeHeatGet', namespace='/data')
def icpe_heat_get(msg):
    heat = DataSQL.icpe.heat.Get(msg['icpe'])
    if heat:
        emit('icpeHeatGet', (heat))
    return True

@socketio.on('sensorHeatGet', namespace='/data')
def icpe_het_get(msg):
    heat = DataSQL.sensor.heat.Get(msg['icpe'], msg['sensor'])
    if heat:
        emit('icpePowerGet', (heat))
    return True
