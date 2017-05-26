@socketio.on('icon', namespace='/zwave')
def zwave_icon(msg):
    if msg['classtype']:
        icon = eval('ZWave.commandclass.' + msg['commandclass'] +
                    msg['classtype'])(msg['value'])
    else:
        icon = eval('ZWave.commandclass.' + msg['commandclass'])(msg['value'])

    emit('icon', {'id' :  msg['id'], 'icon' : msg['icon']})
