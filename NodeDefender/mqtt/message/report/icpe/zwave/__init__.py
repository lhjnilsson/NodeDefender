from NodeDefender.mqtt.message.report.icpe.zwave import info

def event(topic, payload):
    try:
        eval(topic['commandClass'] + '.' + topic['action'])(topic, payload)
    except (NameError, AttributeError):
        print(topic['commandClass'], topic['action'])
