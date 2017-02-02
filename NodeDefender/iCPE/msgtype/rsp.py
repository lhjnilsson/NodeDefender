from .. import db, mqtt
from ..decorators import CommonPayload

def normal(mqttsrc, topic, payload):
    # iCPE Enters Normal Mode
    return True

def include(mqttsrc, topic, payload):
    # iCPE Enters Inclusion Mode
    return True

def exclude(mqttsrc, topic, payload):
    # iCPE Enters Exclusion Mode
    return True

def add(mqttsrc, topic, payload):
    # ZWave Sensor has been Added
    return True

def list(mqttsrc, topic, payload):
    # List of ZWave Sensors
    for sensor in payload.split(','):
        db.sensor.Verify.delay(topic.macaddr, sensor, **mqttsrc)
    return None, None, None, None

@CommonPayload
def qry(mqttsrc, topic, payload):
    # Specific Information about a ZWave Sensor
    if topic.sensorid < '2' or topic.sensorid == 'sys':
        pass
    else:
        for cls in payload.clslist_0.split(','):
            db.cmdclass.Add.delay(topic.macaddr, topic.sensorid, cls)

    return None, None, None, None
