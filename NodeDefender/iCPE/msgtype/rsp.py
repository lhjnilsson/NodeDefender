from .. import db, mqtt
from ..decorators import CommonPayload

def normal(topic, payload, mqttsrc):
    # iCPE Enters Normal Mode
    return True

def include(topic, payload, mqttsrc):
    # iCPE Enters Inclusion Mode
    return True

def exclude(topic, payload, mqttsrc):
    # iCPE Enters Exclusion Mode
    return True

def add(topic, payload, mqttsrc):
    # ZWave Sensor has been Added
    return True

def list(topic, payload, mqttsrc):
    # List of ZWave Sensors
    for sensor in payload.split(','):
        db.sensor.Verify(topic.macaddr, sensor, **mqttsrc)
    return None, None

@CommonPayload
def qry(topic, payload, mqttsrc):
    # Specific Information about a ZWave Sensor
    if topic.sensorid < '2' or topic.sensorid == 'sys':
        pass
    else:
        for cls in payload.clslist_0.split(','):
            db.cmdclass.Add(topic.macaddr, topic.sensorid, cls)

    return None, None

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
