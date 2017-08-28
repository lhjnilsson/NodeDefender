from NodeDefender.icpe import zwave
from NodeDefender import db

def sensor_event(MacAddress, SensorID, CommandClass, **payload):
    if CommandClass == 'info':
        return True
    data = zwave.event(MacAddress, SensorID, CommandClass, **payload)
    if not data:
        return False

    print(data)
    db.field.update(MacAddress, SensorID, data['field']['name'], \
                    **{'value' : data['value'], 'state' : data['state']})
    return True
