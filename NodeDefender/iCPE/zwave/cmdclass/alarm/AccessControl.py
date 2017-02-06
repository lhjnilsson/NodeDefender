def Info():
    return {'type' : 'checkbox', 'readonly' : True, 'name' : 'door'}

def Event(payload):
    if payload.evt == '16':
        payload._retdata['door'] = True
    
    elif payload.evt == '17':
        payload._retdata['door'] = False

    return payload

def Load():
    return {}

def Form():
    pass
