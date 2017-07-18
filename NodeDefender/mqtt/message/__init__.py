from NodeDefender.mqtt.message import report, respond, command, error


@mqtt_to_dict
def event(topic, payload):
    if not db.icpe.get(topic['icpe']):
        db.icpe.create(topic['icpe'])

    if topic['msgType'] == 'rpt':
        report.event(topic, payload)
    elif topic['msgType'] == 'rsp':
        respond.event(topic, payload)
    elif topic['msgType'] == 'cmd':
        command.event(topic, payload)
    elif topic['msgType'] == 'err':
        error.event(topic, payload)
