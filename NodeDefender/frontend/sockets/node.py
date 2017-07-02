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
from ...models.manage import node as NodeSQL
from ...models.manage import icpe as iCPESQL
from ...mail import node as NodeMail
from flask import jsonify, url_for
from geopy.geocoders import Nominatim
from ... import serializer

@socketio.on('nodes', namespace='/node')
def icpeevent(msg):
    emit('nodes', ([node.to_json() for node in NodeSQL.List(msg)]))
    return True

@socketio.on('location', namespace='/node')
def Location(msg):
    node = NodeSQL.Get(name = msg['node'])
    return emit('location', (node.location.to_json()))

@socketio.on('updateGeneral', namespace='/node')
def update_general(msg):
    node = NodeSQL.Get(name = msg['node'])
    node.name = msg['newName']
    NodeSQL.Save(node)
    url = url_for('NodeView.NodesNode', name = serializer.dumps(node.name))
    emit('redirect', (url), namespace='/general')
    return True

@socketio.on('updateLocation', namespace='/node')
def UpdateLocation(msg):
    node = NodeSQL.Get(name = msg['node'])
    node.location.street = msg['street']
    node.location.city = msg['city']
    node.location.latitude = msg['latitude']
    node.location.longitude = msg['longitude']
    NodeSQL.Save(node)
    emit('reload', namespace='/general')
    return True

@socketio.on('coordinates', namespace='/node')
def Coords(msg):
    geo = Nominatim()
    geocords = geo.geocode(msg['city'] + ' ' + msg['street'])
    if geocords:
        latitude = geocords.latitude
        longitude = geocords.longitude
        emit('coordinates', {'street' : msg['street'], 'city' : msg['city'],
                           'latitude' : str(latitude), 'longitude' :
                           str(longitude)})
    else:
         emit('coordinates', {'street' : msg['street'], 'city' : msg['city'],
                           'latitude' : 'Not Found', 'longitude' :
                           'Not Found'})
    return True

@socketio.on('create', namespace='/node')
def Create(msg):
    location = NodeSQL.Location(msg['street'], msg['city'])
    node = NodeSQL.Create(msg['node'], location)
    NodeSQL.Join(node.name, msg['group'])
    try:
        iCPESQL.Join(msg['macaddr'], node.name)
    except LookupError:
        iCPESQL.Create(msg['macaddr'])
        iCPESQL.Join(msg['macaddr'], node.name)
    NodeMail.new_node.delay(msg['group'], msg['node'])
    emit('reload', namespace='/general')
    return True
