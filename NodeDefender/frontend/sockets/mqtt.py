from flask_socketio import emit, send
from ... import socketio, settings, config
from ...models.manage import group as GroupSQL
from ...models.manage import user as UserSQL
from ...models.manage import mqtt as MQTTSQL
from ...models.manage import role as RoleSQL
from ...mail import group as GroupMail
from ...mail import user as UserMail
from ...conn.mqtt import Load as LoadMQTT

@socketio.on('create', namespace='/mqtt')
def create_mqtt(msg):
    mqtt = MQTTSQL.Create(msg['address'], msg['port'])
    if len(msg['username']):
        mqtt.username = msg['username']
        mqtt.password = msg['password']
    group = GroupSQL.Get(msg['group'])
    mqtt.groups.append(group)
    MQTTSQL.Save(mqtt)
    GroupMail.new_mqtt.delay(group.name, mqtt.ipaddr, mqtt.port)
    LoadMQTT([mqtt])
    emit('reload', namespace='/general')
    return True

@socketio.on('list', namespace='/mqtt')
def mqtt_list(msg):
    if 'icpe' in msg:
        icpe = iCPESQL.Get(msg['icpe'])
        emit('list', ([mqtt.ipaddr for mqtt in icpe.mqtt]))
    elif 'group' in msg:
        group = GroupSQL.Get(msg['group'])
        emit('list', ([mqtt.ipaddr for mqtt in group.mqtt]))
    return True

@socketio.on('info', namespace='/mqtt')
def mqtt_info(msg):
    mqtt = MQTTSQL.Get(**msg)
    emit('info', mqtt.to_json())
    return True
