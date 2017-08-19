from functools import wraps
from NodeDefender import db, icpe

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
    return icpe.zwave.event(topic['macAddress'], topic['node'],
                            topic['commandClass'], **payload)
