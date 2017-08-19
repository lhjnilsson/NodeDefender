from NodeDefender.mqtt.command import fire, TopicFormat

def sup(macaddr, sensorid, classname):
    topic = TopicFormat.format(macaddr, sensorid, classname + ':sup', 'get')
    return fire(topic, icpe = macaddr)
