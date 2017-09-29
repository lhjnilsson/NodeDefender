from flask_mail import Message
from flask import render_template, url_for
import NodeDefender
from NodeDefender import serializer
from NodeDefender.mail import mail

@NodeDefender.decorators.mail_enabled
@NodeDefender.decorators.celery_task
def new_group(group):
    if type(group) == str:
        group = NodeDefender.db.group.get(group)

    if group.email == None:
        return False

    msg = Message('Group Created', sender='noreply@nodedefender.com',
                  recipients=[group.email])
    url = url_for('admin_view.admin_group', name = serializer.dumps(group.name))
    msg.body = render_template('mail/group/new_group.txt', group = group, url =
                              url)
    mail.send(msg)
    return True

@NodeDefender.decorators.mail_enabled
@NodeDefender.decorators.celery_task
def new_mqtt(group, mqttip, mqttport):
    group = NodeDefender.db.group.get(group)
    if group is None:
        return False
    if group.email is None:
        return False
    
    mqtt = NodeDefender.db.mqtt.get(mqttip, mqttport)
    if mqtt is None:
        return False

    msg = Message('MQTT {} added to {}'.format(mqtt.host, group.name), sender='noreply@nodedefender.com', recipients=[group.email])
    url = url_for('admin_view.admin_group', name = serializer.dumps(group.name))
    msg.body = render_template('mail/group/new_mqtt.txt', group = group,\
                               mqtt = mqtt, url = url)
    mail.send(msg)
    return True
