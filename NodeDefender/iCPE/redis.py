from .. import Celery, db

def Initialize():
    pass

@celery.task()
def MQTTEvent(topic, payload):
    pass

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

