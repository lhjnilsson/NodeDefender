@socketio.on('icon', namespace='/zwave')
def zwave_icon(msg):
    if msg['classtype']:
        icon = eval('ZWave.cmdclass.' + msg['cmdclass'] +
                    msg['classtype'])(msg['value'])
    else:
        icon = eval('ZWave.cmdclass.' + msg['cmdclass'])(msg['value'])

    emit('icon', {'id' :  msg['id'], 'icon' : msg['icon']})
