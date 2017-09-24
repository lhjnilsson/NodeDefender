from NodeDefender.mqtt.command import fire, topic_format

def qry(macaddr):
    topic = topic_format.format(macaddr, "sys", "svc", "qry")
    return fire(topic, icpe = macaddr)

def telnet(macaddr, enabled):
    topic = topic_format.format(macaddr, "sys", "svc:cli", "set")
    return fire(topic, payload = str(int(enabled)), icpe = macaddr)

def ssh(macaddr, enabled):
    topic = topic_format.format(macaddr, "sys", "svc:ssh", "set")
    return fire(topic, payload = str(int(enabled)), icpe = macaddr)

def web(macaddr, enabled):
    topic = topic_format.format(macaddr, "sys", "svc:web", "st")
    return fire(topic, payload = str(int(enabled)), icpe = macaddr)

def snmp(macaddr, enabled):
    topic = topic_format.format(macaddr, "sys", "svc:snmp", "set")
    return fire(topic, payload = str(int(enabled)), icpe = macaddr)
