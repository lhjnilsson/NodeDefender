

def Event(payload):
    if payload.evt == '16':
        payload.data['door'] = 'Open'
    elif payload.evt == '17':
        payload.data['door'] = 'Closed'

    return payload

def Load():
    return {}

def Form():
    pass
