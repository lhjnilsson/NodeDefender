from .. import db

def status(conninfo, topic, payload):
    sensor = db.sensor.Get(topic.macaddr, topic.sensorid)
    if sensor is None:
        sensor = db.Load(conninfo, topic.macaddr, topic.sensorid)

    evt = zwave.event(payload)
    db.UpdateSensor(topic, sensor, evt)
    return True
