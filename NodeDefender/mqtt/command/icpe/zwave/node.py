from NodeDefender.mqtt.command import fire, topic_format

def list(macaddr):
    topic = topic_format.format(macaddr, "0", "node", "list")
    return fire(topic, icpe = macaddr)
