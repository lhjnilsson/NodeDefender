from .. import ClassTypeInfo

icons = {'16' : 'fa fa-bell', '17' : 'fa fa-bell-slash-o',\
         '1' : 'fa fa-bell', '0' : 'fa fa-bell-slash-o'}


def Fields():
    return {'type' : 'box', 'readonly' : True, 'name' : 'Door/Window'}

def Event(payload):
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

def Icon(value):
    return icons[value]

def Info():
    typeinfo = ClassTypeInfo()
    typeinfo.number = '06'
    typeinfo.name = 'AccessControl'
    typeinfo.fields = True
    return typeinfo

def Load():
    return {}
