from .. import db

def status(mqttsrc, topic, payload):
    sensor = db.sensor.Get(topic.macaddr, topic.sensorid)
    if sensor is None:
        sensor = db.Load(mqttsrc, topic.macaddr, topic.sensorid)

    evt = zwave.event(payload)
    db.UpdateSensor(topic, sensor, evt)
    return True
