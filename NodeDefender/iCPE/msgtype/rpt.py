def status(topic, payload):
    sensor = db.Get(topic.macaddr, topic.sensorid)
    if sensor is None:
        try:
            sensor = sensor.Load(topic.macaddr, topic.sensorid)
        except LookupError as e:
            print("Sensor not found, ", topic.macaddr, topic.sensorid)

    evt = zwave.event(payload)
    db.UpdateSensor(topic, sensor, evt)
    return True
