from functools import wraps
from NodeDefender import db, icpe
from NodeDefender.mqtt.message.respond.sensor import info

def verify_sensor_and_class(func):
    @wraps(func)
    def wrapper(topic, payload):
        if not db.sensor.get(topic['macAddress'], topic['node']):
            db.sensor.create(topic['macAddress'], topic['node'])
        if not db.commandclass.get(topic['macAddress'], topic['node'],\
                                   classname = topic['commandClass']):
            pass
        return func(topic, payload)
    return wrapper

@verify_sensor_and_class
def event(topic, payload):
    if topic['commandClass'] == 'info':
        return eval('info.' + topic['action'])(topic, payload)
    elif topic['subFunction']:
        return True # Modify later
    return icpe.zwave.event(topic, payload)
