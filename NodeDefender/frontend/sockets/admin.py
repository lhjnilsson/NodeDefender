from flask_socketio import emit, send
from NodeDefender import socketio, settings, config
import NodeDefender

@socketio.on('general', namespace='/admin')
def general_info():
    info = {'hostname' : settings.hostname, 'release' : settings.release,
            'uptime' : settings.uptime()}
    emit('general', info)
    return True

@socketio.on('logging', namespace='/admin')
def logging():
    info = {'enabled' : config.logging.enabled(),
            'type' : config.logging.type(),
            'name' : config.logging.name(),
            'server' : config.logging.server(),
            'port' : config.logging.port()}
    return emit('logging', info)

@socketio.on('database', namespace='/admin')
def database():
    info = {'enabled' : config.database.enabled(),
            'engine' : config.database.engine(),
            'server' : config.database.server(),
            'port' : config.database.port(),
            'database' : config.database.db(),
            'file' : config.database.file()}
    return emit('database', info)

@socketio.on('celery', namespace='/admin')
def celery():
    info = {'enabled' : config.celery.enabled(),
            'broker' : config.celery.broker(),
            'server' : config.celery.server(),
            'port' : config.celery.port(),
            'database' : config.celery.database()}
    return emit('celery', info)

@socketio.on('mail', namespace='/admin')
def mail():
    info = {'enabled' : config.mail.enabled(),
            'server' : config.mail.server(),
            'port' : config.mail.port(),
            'tls' : config.mail.tls(),
            'ssl' : config.mail.ssl(),
            'username' : config.mail.username(),
            'password' : config.mail.password()}
    return emit('mail', info)

@socketio.on('mqttCreate', namespace='/admin')
def create(host, port, group):
    try:
        NodeDefender.db.mqtt.create(host, port)
    except AttributeError as e:
        emit('error', e, namespace='/general')
    NodeDefender.db.group.add_mqtt(group, host, port)
    NodeDefender.mail.group.new_mqtt(group, host, port)
    NodeDefender.mqtt.connection.add(host, port)
    emit('reload', namespace='/general')
    return True

@socketio.on('mqttList', namespace='/admin')
def list(group):
    emit('list', NodeDefender.db.mqtt.list(group))
    return True

@socketio.on('mqttInfo', namespace='/admin')
def info(host, port):
    emit('mqttInfo', NodeDefender.db.mqtt.get(host, port).to_json())
    return True
