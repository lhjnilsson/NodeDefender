from flask_socketio import emit, send
from ... import socketio, settings, config
from ...models.manage import group as GroupSQL
from ...models.manage import user as UserSQL
from ...models.manage import mqtt as MQTTSQL
from ...models.manage import role as RoleSQL
from ...mail import group as GroupMail
from ...mail import user as UserMail
from ...conn.mqtt import Load as LoadMQTT

@socketio.on('createMQTT', namespace='/admin')
def create_mqtt(msg):
    mqtt = MQTTSQL.Create(msg['address'], msg['port'])
    if len(msg['username']):
        mqtt.username = msg['username']
        mqtt.password = msg['password']
    group = GroupSQL.Get(msg['group'])
    mqtt.groups.append(group)
    MQTTSQL.Save(mqtt)
    LoadMQTT([mqtt])
    emit('reload', namespace='/general')
    return True

@socketio.on('mqttInfo', namespace='/admin')
def mqtt_info(msg):
    mqtt = MQTTSQL.Get(**msg)
    emit('mqttInfo', mqtt.to_json())
    return True

@socketio.on('groups', namespace='/adminusers')
def Groups(msg):
    groups = GroupSQL.List()
    groupsnames = [group.name for group in groups]
    emit('groupsrsp', (groupsnames))
    return True

@socketio.on('createGroup', namespace='/admin')
def create_group(info):
    if GroupSQL.Get(info['name']):
        emit('error', ('Group exsists'), namespace='/general')
        return False
    group = GroupSQL.Create(info['name'], info['mail'], info['description'])
    GroupSQL.Location(group, info['street'], info['city'])
    GroupMail.new_group.delay(group.name)
    emit('reload', namespace='/general')
    return True

@socketio.on('createUser', namespace='/admin')
def create_user(info):
    user = UserSQL.Create(info['email'])
    user.firstname = info['firstname']
    user.lastname = info['lastname']
    UserSQL.Save(user)
    UserSQL.Lock(info['email'])
    UserSQL.Join(info['email'], info['group'])
    RoleSQL.AddRole(info['email'], info['role'])
    UserMail.create_user.delay(user.email)
    emit('reload', namespace='/general')
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

@socketio.on('loggType', namespace='/admin')
def logg_type():
    emit('loggType', (config.logging.type()))
    return True

@socketio.on('loggFile', namespace='/admin')
def logg_file():
    emit('loggFile', (config.logging.name()))
    return True

@socketio.on('syslogAddress', namespace='/admin')
def logg_address():
    emit('syslogAddress', (config.logging.server()))
    return True

@socketio.on('syslogPort', namespace='/admin')
def logg_port():
    emit('syslogPort', (config.logging.port()))
    return True

@socketio.on('dbEngine', namespace='/admin')
def db_engine():
    emit('dbEngine', (config.database.engine()))
    return True

@socketio.on('dbFile', namespace='/admin')
def db_file():
    emit('dbFile', (config.database.file()))
    return True

@socketio.on('dbServer', namespace='/admin')
def db_server():
    emit('dbServer', (config.database.server()))
    return True

@socketio.on('dbPort', namespace='/admin')
def db_port():
    emit('dbPort', (config.database.port()))
    return True

@socketio.on('celeryBroker', namespace='/admin')
def celery_broker():
    emit('celeryBroker', (config.celery.broker()))
    return True

@socketio.on('celeryServer', namespace='/admin')
def celery_server():
    emit('celeryServer', (config.celery.server()))
    return True

@socketio.on('celeryPort', namespace='/admin')
def celery_port():
    emit('celeryPort', (config.celery.port()))
    return True

@socketio.on('celeryDatabase', namespace='/admin')
def celery_database():
    emit('celeryDatabase', (config.celery.database()))
    return True

@socketio.on('mailServer', namespace='/admin')
def mail_server():
    emit('mailServer', (config.mail.server()))
    return True

@socketio.on('mailPort', namespace='/admin')
def mail_port():
    emit('mailPort', (config.mail.port()))
    return True

@socketio.on('mailTLS', namespace='/admin')
def mail_tls():
    emit('mailTLS', (config.mail.tls()))
    return True

@socketio.on('mailSSL', namespace='/admin')
def mail_ssl():
    emit('mailSSL', (config.mail.ssl()))
    return True


