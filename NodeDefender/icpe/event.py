import NodeDefender

def sensor_event(MacAddress, SensorID, CommandClass, **payload):
    if CommandClass == 'info':
        return True
    data = NodeDefender.icpe.zwave.event(MacAddress, SensorID, \
                                         CommandClass, **payload)
    if not data:
        return False

    print(data)
    NodeDefender.db.field.update(MacAddress, SensorID, data['fields']['name'], \
                    **{'value' : data['value'], 'state' : data['state']})
    return True
