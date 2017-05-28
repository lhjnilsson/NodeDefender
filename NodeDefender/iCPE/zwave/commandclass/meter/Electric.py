from .. import ClassTypeInfo

def Fields():
    return {'type' : 'value', 'readonly' : True, 'name' : 'Watt'}

def Info():
    typeinfo = ClassTypeInfo()
    typeinfo.name = 'Electric'
    typeinfo.number = '1'
    typeinfo.fields = True
    return typeinfo

def Event(payload):
    payload.ccevent = 'Watt'
    payload.value = int(payload.data32, 0) / 10
    return payload
