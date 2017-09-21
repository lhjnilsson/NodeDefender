from NodeDefender.mqtt.command import fire, TopicFormat

def reboot(macaddr):
    topic = topic_format(macaddr, "sys", "sys", "reboot")
    return fire(topic, icpe = macaddr)

def battery(macaddr):
    topic = topic_format(macaddr, "sys", "sys:battery", "qry")
    return fire(topic, icpe = macaddr)

