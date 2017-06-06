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
from flask_login import current_user
from ...mail import group as GroupMail

@socketio.on('create', namespace='/group')
def create(info):
    if GroupSQL.Get(info['name']):
        emit('error', ('Group exsists'), namespace='/general')
        return False
    group = GroupSQL.Create(info['name'], info['mail'], info['description'])
    GroupSQL.Location(group, info['street'], info['city'])
    GroupMail.new_group.delay(group.name)
    emit('reload', namespace='/general')
    return True

@socketio.on('list', namespace='/group')
def list(user):
    user = current_user
    if user is None:
        return
    if user.superuser:
        emit('list', ([group.to_json() for group in GroupSQL.List()]))
    else:
        emit('list', ([group.to_json() for group in user.groups]))
    return True

@socketio.on('info', namespace='/group')
def info(msg):
    group = GroupSQL.Get(msg['name'])
    emit('info', (group.to_json()))
    return True

@socketio.on('addUser', namespace='/group')
def add_user(msg):
    UserSQL.Join(msg['user'], msg['group'])
    emit('Reload')
    return True
