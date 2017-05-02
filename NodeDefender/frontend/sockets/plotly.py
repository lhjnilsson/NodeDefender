from flask_socketio import emit, send, disconnect, join_room, leave_room, \
        close_room, rooms
from ... import socketio
from ...models.manage import data as DataSQL
from ...models.manage import user as UserSQL
from ...models.manage import group as GroupSQL

power_layout = {'title' : '',
               'xaxis' : {'title' : 'Date'},
               'yaxis' : {'title' : 'Power'}
              }

heat_layout = {'title' : '',
               'xaxis' : {'title' : 'Date'},
               'yaxis' : {'title' : 'Heat'}
              }

#Power
@socketio.on('powerChart', namespace='/plotly')
def power_chart(msg):
    user = UserSQL.Get(msg['user'])
    if user.superuser:
        groups = [group.name for group in GroupSQL.List()]
    else:
        groups = [group.name for group in user.groups]

    chart_data = DataSQL.power.Chart(*groups)
    if not chart_data:
        return False

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
    chart_data = DataSQL.group.power.Chart(msg['name'])
    if not chart_data:
        return False

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
def node_power_chart(msg):
    chart_data = DataSQL.node.power.Chart(msg['name'])
    if not chart_data:
        return False

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

@socketio.on('sensorPowerChart', namespace='/plotly')
def sensor_power_chart(msg):
    chart_data = DataSQL.sensor.power.Chart(msg['icpe'], msg['sensor'])
    if not chart_data:
        return False

    data = []
    high = {'name': 'high'}
    low = {'name': 'low'}
    average = {'name': 'average'}

    high['x'] = []
    low['x'] = []
    average['x'] = []
                 
    high['y'] = []
    low['y'] = []
    average['y'] = []
    for x in chart_data['power']:
        high['x'].append(x['date'])
        low['x'].append(x['date'])
        average['x'].append(x['date'])
        
        high['y'].append(x['high'])
        low['y'].append(x['low'])
        average['y'].append(x['average'])
    
    data.append(high)
    data.append(low)
    data.append(average)

    layout = power_layout
    layout['title'] = 'sensor Power'
    emit('sensorPowerChart', {'data': data, 'layout' : layout})
    return True

#Heat
@socketio.on('heatChart', namespace='/plotly')
def heat_chart(msg):
    user = UserSQL.Get(msg['user'])
    if user.superuser:
        groups = [group.name for group in GroupSQL.List()]
    else:
        groups = [group.name for group in user.groups]

    chart_data = DataSQL.heat.Chart(*groups)
    if not chart_data:
        return False

    data = []
    for chart in chart_data:
        d = {'name': chart['name']}
        d['x'] = []
        d['y'] = []
        for x in chart['heat']:
            d['x'].append(x['date'])
            d['y'].append(x['value'])
        data.append(d)
    layout = heat_layout
    layout['title'] = 'Group Heat'
    emit('heatChart', {'data': data, 'layout' : layout})
    return True

@socketio.on('groupHeatChart', namespace='/plotly')
def group_heat_chart(msg):
    chart_data = DataSQL.group.heat.Chart(msg['name'])
    if not chart_data:
        return False

    data = []
    for chart in chart_data:
        d = {'name': chart['name']}
        d['x'] = []
        d['y'] = []
        for x in chart['heat']:
            d['x'].append(x['date'])
            d['y'].append(x['value'])
        data.append(d)
    layout = heat_layout
    layout['title'] = 'Group Heat'
    emit('groupHeatChart', {'data': data, 'layout' : layout})
    return True

@socketio.on('nodeHeatChart', namespace='/plotly')
def node_heat_chart(msg):
    chart_data = DataSQL.node.heat.Chart(msg['name'])
    if not chart_data:
        return False

    data = []
    for chart in chart_data:
        d = {'name': chart['name']}
        d['x'] = []
        d['y'] = []
        for x in chart['heat']:
            d['x'].append(x['date'])
            d['y'].append(x['value'])
        data.append(d)
    layout = heat_layout
    layout['title'] = 'Node Heat'
    emit('nodeHeatChart', {'data': data, 'layout' : layout})
    return True

@socketio.on('sensorHeatChart', namespace='/plotly')
def sensor_heat_chart(msg):
    chart_data = DataSQL.sensor.heat.Chart(msg['icpe'], msg['sensor'])
    if not chart_data:
        return False

    data = []
    high = {'name': 'high'}
    low = {'name': 'low'}
    average = {'name': 'average'}

    high['x'] = []
    low['x'] = []
    average['x'] = []
                 
    high['y'] = []
    low['y'] = []
    average['y'] = []
    for x in chart_data['heat']:
        high['x'].append(x['date'])
        low['x'].append(x['date'])
        average['x'].append(x['date'])
        
        high['y'].append(x['high'])
        low['y'].append(x['low'])
        average['y'].append(x['average'])
    
    data.append(high)
    data.append(low)
    data.append(average)

    layout = heat_layout
    layout['title'] = 'sensor Heat'
    emit('sensorHeatChart', {'data': data, 'layout' : layout})
    return True
