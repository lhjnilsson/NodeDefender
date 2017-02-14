from .. import db, zwave
from ..decorators import CommonPayload
from .decorators import VerifyCmdclass, VerifySensor

@VerifyCmdclass
@CommonPayload
def status(topic, payload, mqttsrc):
    if topic.subfunc:
        return sup(topic, payload, mqttsrc)
    return zwave.Event(topic, payload)

@VerifyCmdclass
@CommonPayload
def event(topic, payload, mqttsrc):
    return zwave.Event(topic, payload)

@VerifyCmdclass
@CommonPayload
def sup(topic, payload, mqttsrc):
    try:
        db.cmdclass.AddTypes(topic.macaddr, topic.sensorid, topic.cmdclass,
                         payload.typelist)
    except AttributeError:
        pass

    return None, None

@VerifySensor
@CommonPayload
def get(topic, payload, mqttsrc):
    if topic.subfunc:
        return eval(topic.subfunc)(topic, payload, mqttsrc)
