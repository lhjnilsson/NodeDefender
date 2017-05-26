from .. import db, zwave
from ..decorators import ParsePayload
from .decorators import VerifyCommandclass, VerifySensor

@VerifyCommandclass
@ParsePayload
def status(topic, payload, mqttsrc):
    if topic.subfunc:
        return sup(topic, payload, mqttsrc)
    return zwave.Event(topic, payload)

@VerifyCommandclass
@ParsePayload
def event(topic, payload, mqttsrc):
    return zwave.Event(topic, payload)

@VerifyCommandclass
@ParsePayload
def sup(topic, payload, mqttsrc):
    try:
        db.commandclass.AddTypes(topic, payload)
    except AttributeError:
        pass

    return None, None

@VerifySensor
@ParsePayload
def get(topic, payload, mqttsrc):
    if topic.subfunc:
        return eval(topic.subfunc)(topic, payload, mqttsrc)
