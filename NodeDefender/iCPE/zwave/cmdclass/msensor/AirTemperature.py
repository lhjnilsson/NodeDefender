def Fields():
    return {'type' : 'value', 'readonly' : True, 'name' : 'celsius'}

def Event(payload):
    payload.name = 'celsius'
    payload.classtype = 'heat'
    if payload.unit != '0':
        return False 
    payload.value = int(payload.data, 0) / 10
    return payload
