def Datafield():
    return {'type' : 'value', 'readonly' : True, 'name' : 'Watt'}

def Event(payload):
    payload.ccevent = 'Watt'
    payload.value = int(payload.data32, 0) / 10
    return payload
