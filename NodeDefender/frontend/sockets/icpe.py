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
from ...models.manage import icpe as iCPESQL

@socketio.on('list', namespace='/icpe')
def List(msg):
    icpes = [icpe.macaddr for icpe in iCPESQL.List(**msg)]
    emit('listRsp', (icpes))
    return True

@socketio.on('unassigned', namespace='/icpe')
def Unassigned(msg):
    icpes = [icpe.macaddr for icpe in iCPESQL.Unassigned(**msg)]
    emit('unassignedRsp', (icpes), namespace='/icpe')
    return True


@socketio.on('info', namespace='/icpe')
def Info(msg):
    icpe = iCPESQL.Get(msg['icpe'])
    if icpe:
        emit('info', (icpe.to_json()))
        return True

@socketio.on('connection', namespace='/icpe')
def connection(msg):
    emit('connection', {'address' : '127.0.0.1', 'type' : 'wired'})
    return True

@socketio.on('power', namespace='/icpe')
def power(msg):
    emit('power', {'source' : 'wired', 'battery' : 'none'})
