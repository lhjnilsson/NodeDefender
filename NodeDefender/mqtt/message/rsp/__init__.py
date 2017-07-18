from NodeDefender.mqtt.message.rsp import zwave, sys, sensor

def event(topic, payload):
    if topic['node'] == '0':
        zwave.event(topic, paylad)
    elif topic['node'] == 'sys':
        sys.event(topic, payload)
    else:
        sensor.event(topic, payload)
