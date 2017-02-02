from .. import db, zwave
from ..decorators import CommonPayload

def status(mqttsrc, topic, payload):
    sensor = db.cmdclass.Verify(topic.macaddr, topic.sensorid,
                                topic.cmdclass, **mqttsrc)
    event = zwave.Event(topic, payload)
    return cmdclass, event

def event(mqttsrc, topic, payload):
    cmdclass = db.cmdclass.Verify(topic.macaddr, topic.sensorid,
                                      topic.cmdclass, **mqttsrc)
    event = zwave.Event(topic, payload)
    return cmdclass, event

@CommonPayload
def sup(mqttsrc, topic, payload):
    db.cmdclass.AddTypes(topic.mac, topic.sensorid, topic.cmdclass,
                         payload.types)
    return None, None
