from .. import db, mqtt
from ..decorators import CommonPayload
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

@VerifyiCPE
@CommonPayload
def qry(topic, payload, mqttsrc):
    # Specific Information about a ZWave Sensor
    if topic.sensorid < '2' or topic.sensorid == 'sys':
        pass
    else:
        db.cmdclass.Add(topic, payload, payload.clslist_0.split(','))

    return None, None

@VerifyiCPE
@CommonPayload
def sup(topic, payload, mqttsrc):
    try:
        db.cmdclass.AddTypes(topic, payload, topic.cmdclass, payload.typelist)
    except AttributeError:
        pass

    return None, None

@VerifySensor
@CommonPayload
def get(topic, payload, mqttsrc):
    if topic.subfunc:
        return eval(topic.subfunc)(topic, payload, mqttsrc)
