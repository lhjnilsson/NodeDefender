from .. import db, zwave

def status(mqttsrc, topic, payload):
    sensor = db.sensor.Verify(topic.macaddr, topic.sensorid, **mqttsrc)
    return zwave.Event(**payload)

def event(mqttsrc, topic, payload):
    sensor = db.sensor.Verify(topic.macaddr, topic.sensorid, **mqttsrc)
    return zwave.Event(**payload)
