from .. import celery, db
from .decorators import TopicToTuple
#from .zwave import Event as ZWaveEvent
from . import db
from .type import *


@celery.task
@TopicToTuple
def MQTT(topic, payload):
    try:
        getattr(topic.type, topic.action)(topic, payload)
    except AttributeError as e:
        print("ERROR", e, topic)
    
    return
    
@celery.task
def JSON(topic, payload):
    pass
