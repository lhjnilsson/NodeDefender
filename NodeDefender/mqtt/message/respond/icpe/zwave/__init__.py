from NodeDefender.mqtt.message.respond.icpe.zwave import info
from NodeDefender.mqtt.message.respond.icpe.zwave import node

def event(topic, payload):
    try:
        eval(topic['commandClass'] + '.' + topic['action'])(topic, payload)
    except NameError:
        print("Respond unsupport CC: ", topic['commandClass'])
