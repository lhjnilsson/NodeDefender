def Fields():
    return {'type' : 'box', 'readonly' : True, 'name' : 'door'}

def Event(payload):
    payload.name = 'door'
    payload.classtype = 'AccessControl'
    if payload.evt == '16':
        payload.value = True
    
    elif payload.evt == '17':
        payload.value = False

    return payload

def Load():
    return {}

def Form():
    pass
