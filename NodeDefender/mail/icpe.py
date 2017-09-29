from flask_mail import Message
from flask import render_template, url_for
import NodeDefender
from NodeDefender import serializer
from NodeDefender.mail import mail

@NodeDefender.decorators.mail_enabled
@NodeDefender.decorators.celery_task
def new_icpe(icpe, host, port):
    icpe = NodeDefender.db.icpe.get(icpe)
    if icpe is None:
        return False

    mqtt = NodeDefender.db.mqtt.get(host, port)
    if mqtt is None:
        return False

    msg = Message('iCPE {} found on MQTT {}'.format(icpe.mac_address, mqtt.host),
                  sender='noreply@nodedefender.com', recipients=\
                  [group.email for group in mqtt.groups ])
    url = url_for('node_view.nodes_list')
    msg.body = render_template('mail/icpe/new_icpe.txt', icpe = icpe, mqtt =
                               mqtt, url = url)
    mail.send(msg)
    return True

@NodeDefender.decorators.mail_enabled
@NodeDefender.decorators.celery_task
def icpe_enabled(icpe, host, port):
    icpe = NodeDefender.db.icpe.get(icpe)
    if icpe is None:
        return False

    mqtt = NodeDefender.db.mqtt.get(host, port)
    if mqtt is None:
        return False

    msg = Message('iCPE {} Enabled from MQTT {}'.format(icpe.mac_address, mqtt.host),
                  sender='noreply@nodedefender.com', recipients=\
                  [group.email for group in mqtt.groups ])
    url = url_for('node_view.nodes_list')
    msg.body = render_template('mail/icpe/icpe_enabled.txt', icpe = icpe, mqtt =
                               mqtt, url = url)
    mail.send(msg)
    return True


