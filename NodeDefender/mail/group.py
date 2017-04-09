from ..models.manage import group as GroupSQL
from .. import serializer, app, celery, mail
from flask_mail import Message
from flask import render_template, url_for

@celery.task
def new_group(group):
    if type(group) == str:
        group = GroupSQL.Get(group)

    if group.email == None:
        return False

    msg = Message('Group Created', sender='noreply@nodedefender.com',
                  recipients=[group.email])
    url = url_for('AdminView.AdminGroup', name = serializer.dumps(group.name))
    msg.body = render_template('mail/group/new_group.txt', group = group, url =
                              url)
    mail.send(msg)
    return True

@celery.task
def new_mqtt(group, mqtt):
    group = GroupSQL.Get(group)
    if group is None:
        return False
    if group.email is None:
        return False
    
    msg = Message('MQTT {} added to {}'.format(mqtt.ipaddr, group.name), sender='noreply@nodedefender.com', recipients=[group.email])
    url = url_for('AdminView.AdminGroup', name = serializer.dumps(group.name))
    msg.body = render_template('mail/group/new_node.txt', group = group, url =
                              url)
    mail.send(msg)
    return True
