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
from ... import socketio
from ...models.manage import group as GroupSQL
from ...models.manage import user as UserSQL
from ...models.manage import role as RoleSQL
from ...mail import user as UserMail
from flask_login import current_user
from flask import flash, redirect, url_for

@socketio.on('create', namespace='/user')
def create(user):
    if not GroupSQL.Get(user['group']):
        emit('error', ('Group does not exist'), namespace='/general')
        return False

    if UserSQL.Get(user['email']):
        emit('error', ('User Exists'), namespace='/general')
        return False
    db_user = UserSQL.Create(user['email'])
    db_user.firstname = user['firstname']
    db_user.lastname = user['lastname']
    UserSQL.Save(db_user)

    UserSQL.Join(db_user.email, user['group'])
    RoleSQL.AddRole(db_user.email, user['role'])
    UserMail.new_user.delay(db_user.email)
    emit('reload', namespace='/general')
    return True

@socketio.on('list', namespace='/user')
def list(user):
    user = current_user
    if user is None:
        return
    if user.superuser:
        emit('list', ([group.to_json() for group in GroupSQL.List()]))
    else:
        emit('list', ([group.to_json() for group in user.groups]))
    return True

@socketio.on('info', namespace='/user')
def info(msg):
    group = GroupSQL.Get(msg['name'])
    emit('info', (group.to_json()))
    return True

@socketio.on('freeze', namespace='/user')
def freeze_user(user):
    pass

@socketio.on('enable', namespace='/user')
def enable_user(user):
    pass

@socketio.on('resetPassword', namespace='/user')
def freeze_user(user):
    pass

@socketio.on('delete', namespace='/user')
def delete_user(user):
    try:
        UserSQL.Delete(user)
    except LookupError:
        emit('error')
        return
    emit('redirect', (url), namespace='/general')
