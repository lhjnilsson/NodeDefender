from .. import db, zwave

def status(mqttsrc, topic, payload):
    sensor = db.sensor.Verify.delay(topic.macaddr, topic.sensorid, **mqttsrc)
    event = event.ZWave.delay(**payload)
    sensor.get()
    event.get()
    return sensor, event

def event(mqttsrc, topic, payload):
    sensor = db.sensor.Verify.delay(topic.macaddr, topic.sensorid, **mqttsrc)
    event.Zwave.delay(**payload)
    sensor.get()
    event.get()
    return sensor, event
