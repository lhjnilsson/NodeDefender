from NodeDefender.mqtt.command import fire, TopicFormat

def list(macaddr):
    topic = TopicFormat.format(macaddr, "0", "node", "list")
    return fire(topic, icpe = macaddr)
