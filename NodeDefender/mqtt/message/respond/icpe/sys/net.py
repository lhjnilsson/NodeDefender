import NodeDefender

def set(topic, payload):
    return NodeDefender.mqtt.icpe.system_info(topic['macAddress'])

def qry(topic, payload):
    dhcp = bool(eval(payload.pop(0)))
    return NodeDefender.db.icpe.update(topic['macAddress'],
                                       **{'ip_dhcp' : dhcp})

def stat(topic, payload):
    address = payload.pop(0)
    subnet = payload.pop(0)
    gateway = payload.pop(0)
    return NodeDefender.db.icpe.update(topic['macAddress'],
                                       **{'ip_address' : address,
                                          'ip_subnet' : subnet,
                                          'ip_gateway' : gateway})
