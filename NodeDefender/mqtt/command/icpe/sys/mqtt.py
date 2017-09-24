from NodeDefender.mqtt.command import fire, topic_format

def set(macaddr, *args):
    topic = topic_format.format(macaddr, "sys", "mqtt", "set")
    payload = list(args)
    return fire(topic, payload = payload, icpe = macaddr)
