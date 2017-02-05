from .. import db, zwave
from ..decorators import CommonPayload

def status(mqttsrc, topic, payload):
    if topic.subfunc:
        return sup(mqttsrc, topic, payload)

    cmdclass = db.cmdclass.Verify(topic.macaddr, topic.sensorid,
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
    try:
        db.cmdclass.AddTypes(topic.macaddr, topic.sensorid, topic.cmdclass,
                         payload.typelist)
    except AttributeError:
        pass

    return None, None

def get(mqttsrc, topic, payload):
    if topic.subfunc:
        return eval(topic.subfunc)(mqttsrc, topic, payload)
