from .. import Celery, db
from .decorators import XMLToDict
from .zwave import Event as ZWaveEvent

def Initialize():
    pass

@celery.task()
@XMLToDict
def MQTTEvent(topic, payload):
    event = ZWaveEvent(payload['commandClass'], payload['value'],
                       payload['evttype'])
    q = Query(CeleryHost, topic['mac']+topic['nodeid'])
    if not q:
        return

@celery.task()
def JSONEvent(topic, payload):
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

