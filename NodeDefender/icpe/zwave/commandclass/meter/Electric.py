def fields():
    return {'type' : 'value', 'readonly' : True, 'name' : 'Watt'}

def info():
    return {'name' : 'Electric',
            'number' : '1',
            'fields' : True}

def icon(value):
    return 'fa fa-plug'

def event(payload):
    payload.field = 'Watt'
    payload.value = int(payload.data32, 0) / 10
    if payload.value > 1.0:
        payload.state = True
    
    payload.icon = 'fa fa-plug'
    return payload
