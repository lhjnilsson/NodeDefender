from NodeDefender.mqtt.command import fire, topic_format

def include(macaddr):
    topic = topic_format.format(macaddr, "0", "mode", "include")
    return fire(topic, icpe = macaddr)

def exclude(macaddr):
    topic = topic_format.format(macaddr, "0", "mode", "exclude")
    return fire(topic, icpe = macaddr)
