from flask_socketio import emit, send, disconnect, join_room, leave_room, \
        close_room, rooms
from ... import socketio
from ...models.manage import data as DataSQL
from ...models.manage import user as UserSQL

power_layout = {'title' : '',
               'xaxis' : {'title' : 'Date'},
               'yaxis' : {'title' : 'Power'}
              }

@socketio.on('powerChart', namespace='/plotly')
def power_chart(msg):
    groups = UserSQL.Groups(msg['user'])

    chart_data = DataSQL.power.Chart(*[group.name for group in groups])
    data = []
    for chart in chart_data:
        d = {'name': chart['name']}
        d['x'] = []
        d['y'] = []
        for x in chart['power']:
            d['x'].append(x['date'])
            d['y'].append(x['value'])
        data.append(d)
    layout = power_layout
    layout['title'] = 'Group Power'
    emit('powerChart', {'data': data, 'layout' : layout})
    return True

@socketio.on('groupPowerChart', namespace='/plotly')
def group_power_chart(msg):
    chart_data = DataSQL.group.power.Chart(msg['group'])

    data = []
    for chart in chart_data:
        d = {'name': chart['name']}
        d['x'] = []
        d['y'] = []
        for x in chart['power']:
            d['x'].append(x['date'])
            d['y'].append(x['value'])
        data.append(d)
    layout = power_layout
    layout['title'] = 'Group Power'
    emit('groupPowerChart', {'data': data, 'layout' : layout})
    return True

@socketio.on('nodePowerChart', namespace='/plotly')
def group_power_chart(msg):
    chart_data = DataSQL.node.power.Chart(msg['node'])

    data = []
    for chart in chart_data:
        d = {'name': chart['name']}
        d['x'] = []
        d['y'] = []
        for x in chart['power']:
            d['x'].append(x['date'])
            d['y'].append(x['value'])
        data.append(d)
    layout = power_layout
    layout['title'] = 'Node Power'
    emit('nodePowerChart', {'data': data, 'layout' : layout})
    return True
