def Fields():
    return {'type' : 'value', 'readonly' : True, 'name' : 'Current Watt'}

def Event(payload):
    payload.name = 'watt'
    payload.classtype = 'power'
    payload.value = int(payload.data32, 0) / 10
    return payload
