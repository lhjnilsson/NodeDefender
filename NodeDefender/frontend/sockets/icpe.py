from flask_socketio import emit, send, disconnect, join_room, leave_room, \
        close_room, rooms
from NodeDefender import socketio
import NodeDefender
from flask_login import current_user

@socketio.on('list', namespace='/icpe')
def list(node):
    emit('list', [icpe.to_json() for icpe in NodeDefender.db.icpe.list(node)])
    return True

@socketio.on('unassigned', namespace='/icpe')
def unassigned():
    icpes = [icpe.to_json() for icpe in
            NodeDefender.db.icpe.unassigned(current_user)]
    emit('unassigned', icpes)
    return True

@socketio.on('info', namespace='/icpe')
def info(icpe):
    emit('info', NodeDefender.db.icpe.get(icpe))
    return True

@socketio.on('connection', namespace='/icpe')
def connection(icpe):
    emit('connection', NodeDefender.db.icpe.connection(icpe))
    return True

@socketio.on('power', namespace='/icpe')
def power(icpe):
    emit('power', NodeDefender.db.icpe.power(icpe))
    return True
