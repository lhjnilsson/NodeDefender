from flask_socketio import emit, send, disconnect, join_room, leave_room, \
        close_room, rooms
from NodeDefender import socketio, serializer
import NodeDefender
from flask import jsonify, url_for
from geopy.geocoders import Nominatim

@socketio.on('create', namespace='/node')
def create(name, group, location):
    NodeDefender.db.node.create(name)
    NodeDefender.db.group.add_node(group, name)
    NodeDefender.db.node.set_location(name, **location)
    NodeDefender.mail.node.new_node(name)
    url = url_for('NodeView.NodesNode', name = serializer.dumps(name))
    emit('redirect', (url), namespace='/general')
    return True

@socketio.on('delete', namespace='/node')
def delete(name):
    NodeDefender.db.node.delete(name)
    url = url_for('NodeView.NodesNodes')
    emit('redirect', (url), namespace='/general')
    return True

@socketio.on('list', namespace='/node')
def list(user_mail):
    emit('list', NodeDefender.db.node.list(user_mail))
    return True

@socketio.on('addiCPE', namespace='/node')
def add_icpe(node_name, icpe_macaddr):
    try:
        NodeDefender.db.node.add_icpe(node_name, icpe_macaddr)
        emit('reload', namespace='/general')
    except KeyError as e:
        emit('error', e, namespace='/general')
    return True

@socketio.on('removeiCPE', namespace='/node')
def remove_icpe(node, macaddr):
    try:
        NodeDefender.db.node.remove_icpe(node_name, icpe_macaddr)
        emit('reload', namespace='/general')
    except KeyError as e:
        emit('error', e, namespace='/general')
    return True

@socketio.on('location', namespace='/node')
def location(name):
    return emit('location', NodeDefender.db.node.get(name).location.to_json())

@socketio.on('update', namespace='/node')
def update_general(name, kwargs):
    NodeDefender.db.node.update(name, **kwargs)
    url = url_for('NodeView.NodesNode', name = serializer.dumps(node.name))
    emit('redirect', (url), namespace='/general')
    return True

@socketio.on('updateLocation', namespace='/node')
def update_location(name, location):
    node = NodeDefender.db.node.get_sql(name)
    node.location.street = location['street']
    node.location.city = location['city']
    node.location.latitude = location['latitude']
    node.location.longitude = location['longitude']
    NodeDefender.db.node.save_sql(node)
    emit('reload', namespace='/general')
    return True

@socketio.on('coordinates', namespace='/node')
def coordinates(msg):
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


