icons = {'16' : 'fa fa-bell', '17' : 'fa fa-bell-slash-o',\
         '1' : 'fa fa-bell', '0' : 'fa fa-bell-slash-o'}

def fields():
    return {'type' : 'box', 'readonly' : True, 'name' : 'Door/Window'}

def event(payload):
    payload.cctype = '06'
    payload.cctypename = 'AccessControl'
    payload.field = 'Door/Window' 

    if payload.evt == '16':
        payload.value = '16'
        payload.state = True
        payload.icon = 'fa fa-bell'
    elif payload.evt == '17':
        payload.value = '17'
        payload.state = False
        payload.icon = 'fa fa-bell-slash-o'

    return payload

def icon(value):
    return icons[value]

def info():
    return {'number' : '06',
            'name' : 'AccessControl',
            'fields' : True}
