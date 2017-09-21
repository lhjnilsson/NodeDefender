from NodeDefender.mqtt.command import fire, TopicFormat

def upgrade(macaddr, *args):
    topic = topic_format.format(macaddr, "sys", "fw", "upgrade")
    payload = list(args)
    return fire(topic, payload = payload, icpe = macaddr)
