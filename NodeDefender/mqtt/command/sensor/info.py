from NodeDefender.mqtt.command import fire, TopicFormat

def qry(macaddr, sensorid):
    topic = TopicFormat.format(macaddr, sensorid, "info", "qry")
    return fire(topic, icpe = macaddr)
