def list(topic, payload):
    for sensor in payload:
        if not db.sensor.get(topic['icpe'], sensor):
            db.sensor.create(topic['icpe'], sensor)

    return True

def update(topic, payload):
    pass


def txnif(topic, payload):
    pass


