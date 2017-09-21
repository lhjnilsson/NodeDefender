from NodeDefender.mqtt.command import fire, TopicFormat

def set(macaddr, *args):
    topic = topic_format(macaddr, "sys", "mqtt", "set")
    payload = list(args)
    return fire(topic, payload = payload, icpe = macaddr)
