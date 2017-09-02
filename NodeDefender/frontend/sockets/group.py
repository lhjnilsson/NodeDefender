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
def list(user):
    return emit('list', NodeDefender.db.group.list(user))

@socketio.on('info', namespace='/group')
def info(name):
    return emit('info', NodeDefender.db.group.get(name).to_json())

@socketio.on('addUser', namespace='/group')
def add_user(group_name, user_mail):
    NodeDefender.db.group.add_user(group_name, user_mail)
    return emit('reload', namespace='/general')

@socketio.on('removeUser', namespace='/group')
def add_user(group_name, user_mail):
    NodeDefender.db.group.remove_user(group_name, user_mail)
    return emit('reload', namespace='/general')


