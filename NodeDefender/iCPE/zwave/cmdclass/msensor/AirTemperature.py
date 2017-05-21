def Datafield():
    return {'type' : 'value', 'readonly' : True, 'name' : 'Celsius'}

def Event(payload):
    payload.ccevent = 'Celsius'
    if payload.unit != '0':
        return False 
    payload.value = int(payload.data, 0) / 10
    return payload
