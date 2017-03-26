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

@socketio.on('groups', namespace='/group')
def Groups(msg):
    groups = GroupSQL.List()
    groupsnames = [group.name for group in groups]
    emit('groupsrsp', (groupsnames))
    return True

@socketio.on('groupInfoGet', namespace='/group')
def GroupInfo(msg):
    group = GroupSQL.Get(msg['name'])
    info = {'name' : group.name,
            'description' : group.description,
            'users' : str(len(group.users)),
            'nodes' : str(len(group.nodes)),
            'created_on' : str(group.created_on),
           }
    emit('groupInfoRsp', (info))
    return True

@socketio.on('addToGroup', namespace='/group')
def AddToGroup(msg):
    UserSQL.Join(msg['user'], msg['group'])
    emit('Reload')
    return True
