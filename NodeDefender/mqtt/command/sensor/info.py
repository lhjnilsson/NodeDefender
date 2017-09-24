from NodeDefender.mqtt.command import fire, topic_format

def qry(macaddr, sensorid):
    topic = topic_format.format(macaddr, sensorid, "info", "qry")
    return fire(topic, icpe = macaddr)
