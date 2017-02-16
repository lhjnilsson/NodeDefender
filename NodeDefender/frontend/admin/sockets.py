from flask_socketio import emit, send
from ... import socketio
from ...models.manage import group as GroupSQL

@socketio.on('groups', namespace='/adminusers')
def Groups(msg):
    groups = GroupSQL.List()
    groupsnames = [group.name for group in groups]
    emit('groupsrsp', {'groups' : groupsnames})
    return True

@socketio.on('groupinfo', namespace='/adminusers')
def GroupInfo(msg):
    print("welcome", msg['name'])
    group = GroupSQL.Get(msg['name'])
    info = {'name' : group.name,
            'description' : group.description,
            'users' : str(len(group.users)),
            'nodes' : str(len(group.nodes)),
            'created_on' : group.created_on,
           }
    emit('groupinfo', {'info' : info})
    return True
