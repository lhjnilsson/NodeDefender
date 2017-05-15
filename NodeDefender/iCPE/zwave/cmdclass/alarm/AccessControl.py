def Fields():
    return {'type' : 'box', 'readonly' : True, 'name' : 'Door/Window'}

def Event(payload):
    payload.name = 'door'
    payload.classtype = 'AccessControl'
    if payload.evt == '16':
        payload.value = '16'
        payload.enabled = True
    
    elif payload.evt == '17':
        payload.value = '17'
        payload.enabled = False

    return payload

def Load():
    return {}

def Form():
    pass
