from .. import db

def status(topic, payload, conninfo):
    print("Status")
    sensor = db.Get(topic.macaddr, topic.sensorid)
    if sensor is None:
        sensor = db.Load(topic.macaddr, topic.sensorid, conninfo)

    evt = zwave.event(payload)
    db.UpdateSensor(topic, sensor, evt)
    return True
