from .. import celery, db
from .decorators import TopicToTuple
#from .zwave import Event as ZWaveEvent
from . import db
from .msgtype import cmd, err, rpt, rsp


@celery.task
@TopicToTuple
def MQTT(topic, payload):
    try:
        eval(topic.msgtype + '.' + topic.action)(topic, payload)
    except (AttributeError, NameError) as e:
        print("ERROR", e, topic)
    
    return
    
@celery.task
def JSON(topic, payload):
    pass
