def Info():
    return {'type' : 'checkbox', 'readonly' : True, 'name' : 'Door'}

def Event(payload):
    if payload.evt == '16':
        payload.data['door'] = 'Open'
        print('Door Open')
    elif payload.evt == '17':
        payload.data['door'] = 'Closed'
        print('Door Closed')

    return payload

def Load():
    return {}

def Form():
    pass
