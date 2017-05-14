from .. import db, zwave
from ..decorators import ParsePayload
from .decorators import VerifyCmdclass, VerifySensor

@VerifyCmdclass
@ParsePayload
def status(topic, payload, mqttsrc):
    if topic.subfunc:
        return sup(topic, payload, mqttsrc)
    return zwave.Event(topic, payload)

@VerifyCmdclass
@ParsePayload
def event(topic, payload, mqttsrc):
    return zwave.Event(topic, payload)

@VerifyCmdclass
@ParsePayload
def sup(topic, payload, mqttsrc):
    try:
        db.cmdclass.AddTypes(topic, payload)
    except AttributeError:
        pass

    return None, None

@VerifySensor
@ParsePayload
def get(topic, payload, mqttsrc):
    if topic.subfunc:
        return eval(topic.subfunc)(topic, payload, mqttsrc)
