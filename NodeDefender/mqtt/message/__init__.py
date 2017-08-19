from NodeDefender.mqtt.message import report, respond, command, error
from functools import wraps
from NodeDefender import db

def mqtt_to_dict(func):
    @wraps(func)
    def wrapper(topic, payload, mqtt):
        topic = topic.split('/')
        NewTopic = {'macAddress' : topic[1][2:]}
        NewTopic['messageType'] = topic[2]
        NewTopic['node'] = topic[4].split(':')[0]
        try:
            NewTopic['endPoint'] = topic[4].split(':')[1]
        except IndexError:
            NewTopic['endPoint'] = None
        NewTopic['commandClass'] = topic[6].split(':')[0]
        try:
            NewTopic['subFunction'] = topic[6].split(':')[1]
        except IndexError:
            NewTopic['subFunction'] = None
        NewTopic['action'] = topic[8]
        
        if '=' not in payload:
            return func(NewTopic, payload, mqtt)

        NewPayload = {}
        for part in payload.split(' '):
            try:
                key, value = part.split('=')
                NewPayload[key] = value
            except ValueError:
                pass
        return func(NewTopic, NewPayload, mqtt)
    return wrapper

@mqtt_to_dict
def event(topic, payload, mqtt):
    if not db.icpe.get(topic['macAddress']):
        db.icpe.create(topic['macAddress'], mqtt)

    if topic['messageType'] == 'rpt':
        report.event(topic, payload)
    elif topic['messageType'] == 'rsp':
        respond.event(topic, payload)
    elif topic['messageType'] == 'cmd':
        command.event(topic, payload)
    elif topic['messageType'] == 'err':
        error.event(topic, payload)
