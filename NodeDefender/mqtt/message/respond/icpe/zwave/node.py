from NodeDefender import db

def list(topic, payload):
    return db.sensor.verify_list(topic['macAddress'], payload)
