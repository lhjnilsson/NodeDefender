from NodeDefender.mqtt.command import fire, topic_format

def qry(macaddr):
    topic = topic_format.format(macaddr, "sys", "info", "qry")
    return fire(topic, icpe = macaddr)
