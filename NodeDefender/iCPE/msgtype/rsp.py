from .. import db, mqtt
from ..decorators import ParsePayload
from .decorators import VerifyiCPE, VerifySensor

@VerifyiCPE
def normal(topic, payload, mqttsrc):
    # iCPE Enters Normal Mode
    return True

@VerifyiCPE
def include(topic, payload, mqttsrc):
    # iCPE Enters Inclusion Mode
    return True

@VerifyiCPE
def exclude(topic, payload, mqttsrc):
    # iCPE Enters Exclusion Mode
    return True

@VerifyiCPE
def add(topic, payload, mqttsrc):
    # ZWave Sensor has been Added
    return True

@VerifyiCPE
def list(topic, payload, mqttsrc):
    # List of ZWave Sensors
    for sensor in payload.split(','):
        if sensor < '2':
            pass
        mqtt.sensor.Query(topic.macaddr, sensor, **mqttsrc)
    return None, None

def set(topic, payload, mqttsrc):
    pass

@VerifyiCPE
@ParsePayload
def qry(topic, payload, mqttsrc):
    # Specific Information about a ZWave Sensor
    if topic.sensorid < '2' or topic.sensorid == 'sys':
        pass
    else:
        db.sensor.Verify(topic, payload, mqttsrc)
        db.commandclass.Add(topic, payload)
    return None, None

@VerifyiCPE
@ParsePayload
def sup(topic, payload, mqttsrc):
    try:
        db.commandclasstype.Add(topic, payload, payload.typelist)
    except AttributeError:
        pass

    return None, None

@VerifySensor
@ParsePayload
def get(topic, payload, mqttsrc):
    if topic.subfunc:
        return eval(topic.subfunc)(topic, payload, mqttsrc)


@ParsePayload
def info(topic, payload, mqttsrc):
    print(topic, payload)
