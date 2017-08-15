icons = {True : 'fa fa-toggle-on', False : 'fa fa-toggle-off'}

def info(classtype = None):
    return {'number' : '25',
            'name' : 'bswitch',
            'types' : False}

def fields():
    return {'type' : 'switch', 'readonly' : False, 'name' : 'Switch'}
 
def load(classtypes):
    return {'bswitch' : None}

def icon(value):
    return icons[eval(value)]

def event(payload):
    payload.field = 'Switch'
    if payload.value == '0':
        payload.value = False
        payload.state = False
        payload.icon = 'fa fa-toggle-off'
    
    else:
        payload.value = True
        payload.state = True
        payload.icon = 'fa fa-toggle-on'

    return payload
