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
from NodeDefender import socketio
import NodeDefender
from flask_login import current_user
from flask import flash, redirect, url_for

@socketio.on('create', namespace='/user')
def create(mail, firstname, lastname, group, role):
    if not NodeDefender.db.group.get(group):
        emit('error', ('Group does not exist'), namespace='/general')
        return False

    if NodeDefender.db.user.get(mail):
        emit('error', ('User Exists'), namespace='/general')
        return False

    user = NodeDefender.db.user.create(mail, firstname, lastname)
    NodeDefender.db.group.add_user(group, mail)
    NodeDefender.db.user.set_role(mail, role)
    NodeDefender.mail.user.new_user(user)
    emit('reload', namespace='/general')
    return True

@socketio.on('groups', namespace='/groups')
def groups(mail):
    return emit('groups', NodeDefender.db.user.groups(mail))

@socketio.on('update', namespace='/user')
def update_name(mail, kwargs):
    NodeDefender.db.user.update(mail, **kwargs)
    emit('reload', namespace='/general')
    return True

@socketio.on('freeze', namespace='/user')
def freeze_user(mail):
    return emit('freeze', NodeDefender.db.user.freeze(mail))

@socketio.on('enable', namespace='/user')
def enable_user(mail):
    return emit('enable', NodeDefender.db.user.enable(mail))

@socketio.on('resetPassword', namespace='/user')
def freeze_user(mail):
    return emit('resetPassword', NodeDefender.db.user.reset_password(mail))

@socketio.on('delete', namespace='/user')
def delete_user(mail):
    try:
        NodeDefender.db.user.delete(mail)
    except LookupError:
        emit('error')
        return
    url = url_for('AdminView.AdminUsers')
    emit('redirect', (url), namespace='/general')
