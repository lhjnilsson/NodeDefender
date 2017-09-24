from NodeDefender.mqtt.command import fire, topic_format

def sup(macaddr, sensorid, classname):
    topic = topic_format.format(macaddr, sensorid, classname + ':sup', 'get')
    return fire(topic, icpe = macaddr)
