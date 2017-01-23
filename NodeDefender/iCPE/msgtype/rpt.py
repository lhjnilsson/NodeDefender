from .. import db, zwave

def status(mqttsrc, topic, payload):
    sensor = db.sensor.Get(topic.macaddr, topic.sensorid)
    if sensor is None:
        sensor = db.Load(mqttsrc, topic.macaddr, topic.sensorid)

    return zwave.Event(**payload)

def event(mqttsrc, topic, payload):
    sensor = db.sensor.Get(topic.macaddr, topic.sensorid)
    if sensor is None:
        sensor = db.Load(mqttsrc, topic.macaddr, topic.sensorid)

    return zwave.Event(**payload)
