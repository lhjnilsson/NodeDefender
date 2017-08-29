from functools import wraps
import NodeDefender
from NodeDefender.mqtt.message.report.sensor import info

def verify_sensor_and_class(func):
    @wraps(func)
    def wrapper(topic, payload):
        if not NodeDefender.db.sensor.get(topic['macAddress'], topic['node']):
            NodeDefender.db.sensor.create(topic['macAddress'], topic['node'])
        if not NodeDefender.db.commandclass.get(\
                                topic['macAddress'], topic['node'],\
                                classname = topic['commandClass']):
            pass
        return func(topic, payload)
    return wrapper

@verify_sensor_and_class
def event(topic, payload):
    if topic['commandClass'] == 'info':
        return eval('info.' + topic['action'])(topic, payload)
    elif topic['subFunction']:
        if topic['subFunction'] == 'sup':
            return info.sup(topic, payload)
        elif topic['subFunction'] == 'evtsup':
            return info.evtsup(topic, payload)
    return NodeDefender.icpe.event.sensor_event(topic['macAddress'], topic['node'],\
                                                topic['commandClass'], **payload)
