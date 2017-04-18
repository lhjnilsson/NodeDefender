def Fields():
    return {'type' : 'value', 'readonly' : True, 'name' : 'celsius'}

def Event(payload):
    payload.name = 'celsius'
    payload.classtype = 'heat'
    payload.value = int(payload.data32, 0) / 10
    return payload
