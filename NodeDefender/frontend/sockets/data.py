from flask_socketio import emit, send, disconnect, join_room, leave_room, \
        close_room, rooms
from ... import socketio
from ...models.manage import data as DataSQL
from ...models.manage import user as UserSQL

# Events
@socketio.on('groupEventGet', namespace='/data')
def group_events(msg):
    events = DataSQL.group.event.Get(msg['group'], msg['length'])
    if events:
        emit('groupEventGet', ([event.to_json() for event in events]))
    return True

@socketio.on('nodeEvents', namespace='/data')
def icpe_events(msg):
    events = DataSQL.node.event.Get(msg['node'], msg['length'])
    if events:
        emit('nodeEvents', ([event.to_json() for event in events]))
    return True

@socketio.on('sensorEvents', namespace='/data')
def sensor_events(msg):
    events = DataSQL.sensor.event.Get(msg['icpe'], msg['sensor'])
    if events:
        emit('sensorEvents', ([event.to_json() for event in events]))
    return True

# Power
@socketio.on('groupPowerAverage', namespace='/data')
def group_power_average(msg):
    data = DataSQL.group.power.Average(msg['name'])
    emit('groupPowerAverage', (data))
    return True

@socketio.on('nodePowerAverage', namespace='/data')
def node_power_average(msg):
    data = DataSQL.node.power.Average(msg['name'])
    emit('nodePowerAverage', (data))
    return True

@socketio.on('sensorPowerAverage', namespace='/data')
def sensor_power_average(msg):
    data = DataSQL.sensor.power.Average(msg['icpe'], msg['sensor'])
    emit('sensorPowerAverage', (data))
    return True


# Heat
@socketio.on('groupHeatAverage', namespace='/data')
def group_heat_average(msg):
    data = DataSQL.group.heat.Average(msg['name'])
    emit('groupHeatAverage', (data))
    return True

@socketio.on('nodeHeatAverage', namespace='/data')
def node_heat_average(msg):
    data = DataSQL.node.heat.Average(msg['name'])
    emit('nodeHeatAverage', (data))
    return True

@socketio.on('sensorHeatAverage', namespace='/data')
def sensor_heat_average(msg):
    data = DataSQL.sensor.heat.Average(msg['icpe'], msg['sensor'])
    emit('sensorHeatAverage', (data))
    return True



