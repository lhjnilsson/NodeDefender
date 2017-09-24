from NodeDefender.mqtt.command import fire, topic_format

def set(macaddr, *args):
    topic = topic_format.format(macaddr, "sys", "time:ntp", "set")
    payload = list(args)
    return fire(topic, payload = payload, icpe = macaddr)

def qry(macaddr):
    topic = topic_format.format(macaddr, "sys", "time:ntp", "qry")
    return fire(topic, icpe = macaddr)
