from .. import db, zwave
from ..decorators import CommonPayload

def status(topic, payload, mqttsrc):
    if topic.subfunc:
        return sup(topic, payload, mqttsrc)

    cmdclass = db.cmdclass.Verify(topic, payload, mqttsrc)
    event = zwave.Event(topic, payload)
    return cmdclass, event

def event(topic, payload, mqttsrc):
    cmdclass = db.cmdclass.Verify(topic, payload, mqttsrc)
    event = zwave.Event(topic, payload)
    return cmdclass, event

@CommonPayload
def sup(topic, payload, mqttsrc):
    try:
        db.cmdclass.AddTypes(topic.macaddr, topic.sensorid, topic.cmdclass,
                         payload.typelist)
    except AttributeError:
        pass

    return None, None

def get(topic, payload, mqttsrc):
    if topic.subfunc:
        return eval(topic.subfunc)(topic, payload, mqttsrc)
