from .. import ClassTypeInfo

def Fields():
    return {'type' : 'box', 'readonly' : True, 'name' : 'Door/Window'}

def Event(payload):
    payload.field = 'Door/Window' 
    if payload.evt == '16':
        payload.value = '16'
    elif payload.evt == '17':
        payload.value = '17'

    return payload

def Info():
    typeinfo = ClassTypeInfo()
    typeinfo.number = '06'
    typeinfo.name = 'AccessControl'
    typeinfo.fields = True
    return typeinfo

def Load():
    return {}
