from flask_socketio import emit, send, disconnect, join_room, leave_room, \
        close_room, rooms
from NodeDefender import socketio
import NodeDefender

@socketio.on('list', namespace='/sensor')
def list(icpe):
    emit('list', NodeDefender.db.sensor.list(icpe))
    return True

@socketio.on('info', namespace='/sensor')
def info(icpe, sensor):
    emit('info', NodeDefender.db.sensor.get(icpe, sensor))
    return True

@socketio.on('update', namespace='/sensor')
def update_fields(icpe, sensor, kwargs):
    NodeDefender.db.sensor.update(icpe, sensor, **kwargs)
    emit('reload', namespace='/general')
    return True

@socketio.on('fields', namespace='/sensor')
def fields(icpe, sensor):
    emit('fields', NodeDefender.db.sensor.fields(icpe, sensor))
    return True

@socketio.on('set', namespace='/sensor')
def set(mac_address, sensor_id, commandclass, payload):
    NodeDefender.mqtt.command.sensor.set(mac_address, sensor_id, commandclass,
                                         payload = payload)
    return True

