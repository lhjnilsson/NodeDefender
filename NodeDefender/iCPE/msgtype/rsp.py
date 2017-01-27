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
    print(payload)
    for sensor in payload.split(','):
        if db.sensor.Get(topic.macaddr, sensor) is None:
            mqtt.sensor.Query(topic.macaddr, sensor, **mqttsrc)

def qry(mqttsrc, topic, payload):
    # Specific Information about a ZWave Sensor
    if topic.sensorid == '0':
        return True

    return db.cmdclass.Add(topic.macaddr, topic.sensorid,
                                  *payload['clslist_0'].split(','))
