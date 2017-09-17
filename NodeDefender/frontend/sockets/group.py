from flask_socketio import emit, send, disconnect, join_room, leave_room, \
        close_room, rooms
from NodeDefender import socketio, serializer
import NodeDefender
from flask_login import current_user
from flask import url_for

@socketio.on('create', namespace='/group')
def create(name, mail, description, location):
    if NodeDefender.db.group.get(name):
        emit('error', ('Group exsists'), namespace='/general')
        return False
    group = NodeDefender.db.group.create(name, mail, description)
    NodeDefender.db.group.location(name, **location)
    NodeDefender.mail.group.new_group(name)
    url = url_for('AdminView.AdminGroup', name = serializer.dumps(name))
    return emit('redirect', (url), namespace='/general')

@socketio.on('list', namespace='/group')
def list(user = None):
    if user is None:
        user = current_user.email
    return emit('list',  [group.name for group in
                      NodeDefender.db.group.list(user_mail = user)])

@socketio.on('info', namespace='/group')
def info(name):
    group = NodeDefender.db.group.get(name)
    if group:
        group = group.to_json()
        return emit('info', group)
    else:
        print("Group: ", name)

@socketio.on('addUser', namespace='/group')
def add_user(group_name, user_mail):
    NodeDefender.db.group.add_user(group_name, user_mail)
    return emit('reload', namespace='/general')

@socketio.on('removeUser', namespace='/group')
def add_user(group_name, user_mail):
    NodeDefender.db.group.remove_user(group_name, user_mail)
    return emit('reload', namespace='/general')
