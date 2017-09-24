from NodeDefender.mqtt.command import fire, topic_format

def save(macaddr):
    topic = topic_format.format(macaddr, 'sys', 'config', 'save')
    return fire(topic, icpe = macaddr)

def default(macaddr):
    topic = topic_format.format(macaddr, 'sys', 'config', 'default')
    return fire(topic, icpe = macaddr)

def backup(macaddr, *args):
    payload = list(args)
    topic = topic_format.format(macaddr, 'sys', 'config', 'backup')
    return fire(topic, payload = payload, icpe = macaddr)

def restore(macaddr, *args):
    payload = list(args)
    topic = topic_format.format(macaddr, 'sys', 'config', 'restore')
    return fire(topic, payload = payload, icpe = macaddr)
