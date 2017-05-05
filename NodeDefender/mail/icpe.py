from ..models.manage import icpe as iCPESQL
from ..models.manage import mqtt as MQTTSQL
from .. import serializer, app, celery, mail
from flask_mail import Message
from flask import render_template, url_for

@celery.task
def new_icpe(icpe, ipaddr, port):
    icpe = iCPESQL.Get(icpe)
    if icpe is None:
        return False

    mqtt = MQTTSQL.Get(ipaddr, port)
    if mqtt is None:
        return False

    msg = Message('iCPE {} found on MQTT {}'.format(icpe.macaddr, mqtt.ipaddr),
                  sender='noreply@nodedefender.com', recipients=\
                  [group.email for group in mqtt.groups ])
    url = url_for('NodeView.NodesList')
    msg.body = render_template('mail/icpe/new_icpe.txt', icpe = icpe, mqtt =
                               mqtt, url = url)
    mail.send(msg)
    return True

@celery.task
def icpe_enabled(icpe, ipaddr, port):
    icpe = iCPESQL.Get(icpe)
    if icpe is None:
        return False

    mqtt = MQTTSQL.Get(ipaddr, port)
    if mqtt is None:
        return False

    msg = Message('iCPE {} Enabled from MQTT {}'.format(icpe.macaddr, mqtt.ipaddr),
                  sender='noreply@nodedefender.com', recipients=\
                  [group.email for group in mqtt.groups ])
    url = url_for('NodeView.NodesList')
    msg.body = render_template('mail/icpe/icpe_enabled.txt', icpe = icpe, mqtt =
                               mqtt, url = url)
    mail.send(msg)
    return True

