from NodeDefender.mqtt.messages.rsp

def event(topic, payload):
    eval(topic['class'] + '.' + topic['action'])(topic, payload)
