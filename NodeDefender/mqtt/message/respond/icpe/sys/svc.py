import NodeDefender

def qry(topic, payload):
    telnet = bool(eval(payload.pop(0)))
    http = bool(eval(payload.pop(0)))
    snmp = bool(eval(payload.pop(0)))
    ssh = bool(eval(payload.pop(0)))
    return NodeDefender.db.icpe.update(topic['macAddress'],
                                       **{'telnet' : telnet,
                                          'http' : http,
                                          'snmp' : snmp,
                                          'ssh' : ssh})

def cli(topic, payload):
    enabled = bool(eval(payload))
    return NodeDefender.db.icpe.update(topic['macAddress'],
                                       **{'telnet' : telnet})
def web(topic, payload):
    enabled = bool(eval(payload))
    return NodeDefender.db.icpe.update(topic['macAddress'],
                                       **{'http' : telnet})
def snmp(topic, payload):
    enabled = bool(eval(payload))
    return NodeDefender.db.icpe.update(topic['macAddress'],
                                       **{'snmp' : telnet})
def ssh(topic, payload):
    enabled = bool(eval(payload))
    return NodeDefender.db.icpe.update(topic['macAddress'],
                                       **{'ssh' : telnet})
