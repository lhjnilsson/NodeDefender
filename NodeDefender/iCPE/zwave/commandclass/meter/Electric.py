from .. import ClassTypeInfo

def Fields():
    return {'type' : 'value', 'readonly' : True, 'name' : 'Watt'}

def Info():
    typeinfo = ClassTypeInfo()
    typeinfo.name = 'Electric'
    typeinfo.number = '1'
    typeinfo.fields = True
    return typeinfo

def Icon(value):
    return 'fa fa-plug'

def Event(payload):
    payload.field = 'Watt'
    payload.value = int(payload.data32, 0) / 10
    if payload.value > 1.0:
        payload.state = True
    
    payload.icon = 'fa fa-plug'
    return payload
