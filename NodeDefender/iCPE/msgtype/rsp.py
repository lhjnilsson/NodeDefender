from .. import db, mqtt

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
        if db.sensor.Get(topic.macaddr, sensor) is None:
            mqtt.sensor.Query(topic.macaddr, sensor, **mqttsrc)

def qry(mqttsrc, topic, payload):
    # Specific Information about a ZWave Sensor
    if db.sensor.Get(topic.macaddr, topic.sensorid):
        return True # It's Known
    for cls in payload['clslist_0']:
        db.sensor.AddClass(cls)
    
    return True
