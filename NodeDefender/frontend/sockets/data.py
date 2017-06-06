from flask_socketio import emit, send, disconnect, join_room, leave_room, \
        close_room, rooms
from ... import socketio
from ...models.manage import data as DataSQL
from ...models.manage import user as UserSQL
from ...models.manage import message as MessageSQL
from flask_login import current_user

# Messages
@socketio.on('messages', namespace='/data')
def messages():
    messages = MessageSQL.messages(current_user)
    return emit('messages', ([message.to_json() for message in messages]))

@socketio.on('groupMessages', namespace='/data')
def group_messages(group):
    messages = MessageSQL.group_messages(group)
    return emit('messages', ([message.to_json() for message in messages]))

@socketio.on('nodeMessages', namespace='/data')
def node_messages(node):
    messages = MessageSQL.node_messages(node)
    return emit('messages', ([message.to_json() for message in messages]))

@socketio.on('userMessages', namespace='/data')
def user_messages(user):
    return emit('messages', MessageSQL.messages(user))

# Events
@socketio.on('groupEventsAverage', namespace='/data')
def group_events(group, length = None):
    events = DataSQL.group.event.Average(group)
    emit('groupEventsAverage', (events))
    return True

@socketio.on('groupEventsList', namespace='/data')
def group_events(group, length = None):
    events = DataSQL.group.event.List(group, length)
    if events:
        events = [event.to_json() for event in events]
        emit('groupEventsList', (events))
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
def group_power_average(group):
    data = DataSQL.group.power.Average(group)
    emit('groupPowerAverage', (data))
    return True

@socketio.on('nodePowerAverage', namespace='/data')
def node_power_average(msg):
    data = DataSQL.node.power.Average(msg['name'])
    emit('nodePowerAverage', (data))
    return True

@socketio.on('nodePowerCurrent', namespace='/data')
def node_power_current(msg):
    data = DataSQL.node.power.Current(msg['name'])
    emit('nodePowerCurrent', (data))
    return True

@socketio.on('sensorPowerAverage', namespace='/data')
def sensor_power_average(msg):
    data = DataSQL.sensor.power.Average(msg['icpe'], msg['sensor'])
    emit('sensorPowerAverage', (data))
    return True


# Heat
@socketio.on('groupHeatAverage', namespace='/data')
def group_heat_average(group):
    data = DataSQL.group.heat.Average(group)
    emit('groupHeatAverage', (data))
    return True

@socketio.on('nodeHeatAverage', namespace='/data')
def node_heat_average(msg):
    data = DataSQL.node.heat.Average(msg['name'])
    emit('nodeHeatAverage', (data))
    return True

@socketio.on('nodeHeatCurrent', namespace='/data')
def node_heat_current(msg):
    data = DataSQL.node.heat.Current(msg['name'])
    emit('nodeHeatCurrent', (data))
    return True

@socketio.on('sensorHeatAverage', namespace='/data')
def sensor_heat_average(msg):
    data = DataSQL.sensor.heat.Average(msg['icpe'], msg['sensor'])
    emit('sensorHeatAverage', (data))
    return True



