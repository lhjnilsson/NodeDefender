def normal(topic, payload):
    # iCPE Enters Normal Mode
    logg.iCPE('Enter Normal Mode')
    return

def include(topic, payload):
    # iCPE Enters Inclusion Mode
    logg.iCPE('Enter Include Mode')
    return

def exclude(topic, payload):
    # iCPE Enters Exclusion Mode
    logg.iCPE('Enter Exclude Mode')
    return

def add(topic, payload):
    # ZWave Sensor has been Added
    pass

def del(topic, payload):
    # ZWave Sensor has been Deleted
    pass

def list(topic, payload):
    # List of ZWave Sensors
    for sensor in payload.split(','):
        if db.get(topic.mac + sensor) is None:
            sensor.qry(topic.mac, sensor)

def qry(topic, payload):
    # Specific Information about a ZWave Sensor
    if db.get(topic.mac + topic.sensor):
        return # It's Known
    
    i = icpe.Get(topic.mac)
    if i is None:
        return # iCPE is yet not registered

    sensor.Create(i) # To be added
