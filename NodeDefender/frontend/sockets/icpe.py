from flask_socketio import emit, send, disconnect, join_room, leave_room, \
        close_room, rooms
from NodeDefender import socketio
import NodeDefender
from flask_login import current_user

@socketio.on('list', namespace='/icpe')
def list(node):
    data = {}
    data['node'] = NodeDefender.db.node.get(node).to_json()
    data['icpes'] = [icpe.to_json() for icpe in
                     NodeDefender.db.icpe.list(node)]
    emit('list', data)
    return True

@socketio.on('unassigned', namespace='/icpe')
def unassigned():
    icpes = [icpe.macaddr for icpe in
            NodeDefender.db.icpe.unassigned(current_user)]
    emit('unassigned', icpes)
    return True

@socketio.on('get', namespace='/icpe')
def info(icpe):
    emit('get', NodeDefender.db.icpe.get(icpe))
    return True

@socketio.on('connection', namespace='/icpe')
def connection(icpe):
    emit('connection', NodeDefender.icpe.system.network_settings(icpe))
    return True

@socketio.on('power', namespace='/icpe')
def power(icpe):
    #emit('power', NodeDefender.icpe.system.battery_info(icpe))
    return True

@socketio.on('includeSensor', namespace='/icpe')
def include_sensor(icpe):
    NodeDefender.mqtt.command.icpe.include_mode(icpe)
    return emit('info', 'Include Mode', namespace='/general')

@socketio.on('excludeSensor', namespace='/icpe')
def exclude_sensor(icpe):
    NodeDefender.mqtt.command.icpe.exclude_mode(icpe)
    return emit('info', 'Exclude Mode', namespace='/general')

@socketio.on('mqttUpdate', namespace='/icpe')
def update(icpe):
    NodeDefender.mqtt.command.icpe.system_info(icpe)
    NodeDefender.mqtt.command.icpe.zwave_info(icpe)
    return emit('info', 'iCPE Updated', namespace='/general')
