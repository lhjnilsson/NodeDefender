from NodeDefender.mqtt.command import fire, TopicFormat

def qry(macaddr):
    topic = topic_format(macaddr, "sys", "alarm", "qry")
    return fire(topic, icpe = macaddr)
