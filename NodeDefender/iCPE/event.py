from .. import celery
from . import zwave
from .decorators import TopicToTuple
from .decorators import PayloadToDict

ZWave = celery.task(zwave.Event)

@celery.task
@TopicToTuple
@PayloadToDict
def MQTT(mqttsrc, topic, payload):
    if topic.msgtype == 'cmd':
        return
    db.cmdclass.Verify.delay(topic.macaddr, topic.sensorid, **mqttsrc)
    evt = eval(topic.msgtype + '.' + topic.action)(mqttsrc, topic, payload)
    
    if evt:
        logger.info("Updating info for: {}:{}. Event: {}".\
                    format(topic.macaddr, topic.sensorid, evt))
        return CmdclassRedis.Save(topic.macaddr, topic.sensorid,
                                  topic.cmdclass, **evt)
    else:
        return None
