from .. import celery, db
from .decorators import TopicToTuple
#from .zwave import Event as ZWaveEvent
from . import db
from .msgType import *

def Initialize():
    pass

@celery.task
@TopicToTuple
def MQTT(topic, payload):
    try:
        getattr(topic.msgType, topic.action)(topic, payload)
    except AttributeError:
        print("ERROR", topic)
    return
    
    try:
        int(topic.nodeid)
        ZWaveEvent(topic, payload)
    except ValueError:
        sys.event(topic, payload)

@celery.task
def JSON(topic, payload):
    pass

def Query(hostname, key):
    conn = redis.Redis(hostname)
    q = conn.hgetall(key)
    if len(value):
        return q
    else:
        return False

def Set(hostname, key, **kwargs):
    pass
