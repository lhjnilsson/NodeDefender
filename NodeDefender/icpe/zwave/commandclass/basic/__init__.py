icons = {True : 'fa fa-toggle-on', False : 'fa fa-toggle-off'}

def info(classtype = None):
    return {'name' : 'basic',
            'number' : '20',
            'types' : False}

def fields():
    return {'type' : 'box', 'readonly' : True, 'name' : 'Basic'}

def load(classtypes):
    return {'basic' : None}

def icon(value):
    return icons[eval(value)]

def event(payload):
    payload.field = 'Basic'
    if payload.value == '0x00':
        payload.value = False
        payload.enabled = False
    else:
        payload.value = True
        payload.enabled = True

    return payload
