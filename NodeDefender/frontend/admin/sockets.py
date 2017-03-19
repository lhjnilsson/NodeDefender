from flask_socketio import emit, send
from ... import socketio, settings
from ...models.manage import group as GroupSQL
from ...models.manage import user as UserSQL

@socketio.on('groups', namespace='/adminusers')
def Groups(msg):
    groups = GroupSQL.List()
    groupsnames = [group.name for group in groups]
    emit('groupsrsp', (groupsnames))
    return True

@socketio.on('groupInfoGet', namespace='/adminusers')
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

@socketio.on('addToGroup', namespace='/adminusers')
def AddToGroup(msg):
    UserSQL.Join(msg['user'], msg['group'])
    emit('Reload')
    return True

@socketio.on('generalInfo', namespace='/admin')
def general_info():
    info = {'hostname' : settings.hostname, 'release' : settings.release,
            'uptime' : settings.uptime()}
    emit('generalInfo', info)
    return True
