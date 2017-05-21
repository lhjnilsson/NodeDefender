def Datafield():
    return {'type' : 'box', 'readonly' : True, 'name' : 'Door/Window'}

def Event(payload):
    payload.ccevent = 'Door/Window'
    
    if payload.evt == '16':
        payload.value = '16'
    elif payload.evt == '17':
        payload.value = '17'

    return payload

def Load():
    return {}
