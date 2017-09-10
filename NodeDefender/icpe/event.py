import NodeDefender

def sensor_event(mac_address, sensor_id, CommandClass, **payload):
    if CommandClass == 'info':
        return True
    data = NodeDefender.icpe.zwave.event(mac_address, sensor_id, \
                                         CommandClass, **payload)
    if not data:
        return False

    commandclass = data['commandclass']['name']
    commandclasstype = data['commandclasstype']['name']\
            if data['commandclasstype'] else None

    NodeDefender.db.field.update(mac_address, sensor_id, data['fields']['name'], \
                    **{'value' : data['value'], 'state' : data['state']})
    NodeDefender.db.data.sensor.event.put(mac_address, sensor_id,\
                                       commandclass, commandclasstype,\
                                       data['state'], data['value'])
    return True
