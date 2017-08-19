from NodeDefender.mqtt.command import fire, TopicFormat

def qry(macaddr):
    topic = TopicFormat.format(macaddr, "0", "info", "qry")
    return fire(topic, icpe = macaddr)
