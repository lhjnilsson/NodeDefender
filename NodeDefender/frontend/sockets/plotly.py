from flask_socketio import emit, send, disconnect, join_room, leave_room, \
        close_room, rooms
from ... import socketio
from ...models.manage import data as DataSQL

power_layout = {'title' : '',
               'xaxis' : {'title' : 'Date'},
               'yaxis' : {'title' : 'Power'}
              }



@socketio.on('groupPowerNodes', namespace='/plotly')
def group_power_latest(msg):
    data = []
    power = DataSQL.group.power.Nodes(msg['group'])
    for entry in power:
        d = {'name': entry['node']}
        d['x'] = []
        d['y'] = []
        for x in entry['data']:
            d['x'].append(x['date'])
            d['y'].append(x['power'])
        data.append(d)
    layout = power_layout
    layout['title'] = 'Node Power'
    emit('groupPowerNodes', {'data': data, 'layout' : layout})
    return True
