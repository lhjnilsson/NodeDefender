from NodeDefender.mqtt.message.report.icpe.zwave import info

def event(topic, payload):
    try:
        eval(topic['commandClass'] + '.' + topic['action'])(topic, payload)
    except NameError:
        print(topic['commandClass'])
