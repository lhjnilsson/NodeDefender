def fields():
    return {'type' : 'value', 'readonly' : True, 'name' : 'Celsius'}

def info():
    return {'number' : '1',
            'name' : 'AirTemperature',
            'fields' : True}

def event(payload):
    payload.field = 'Celsius'
    if payload.unit != '0':
        return False 
    payload.value = int(payload.data, 0) / 10
    return payload
