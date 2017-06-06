from .. import ClassTypeInfo

def Fields():
    return {'type' : 'value', 'readonly' : True, 'name' : 'Celsius'}

def Info():
    typeinfo = ClassTypeInfo()
    typeinfo.number = '1'
    typeinfo.name = 'AirTemperature'
    typeinfo.fields = True
    return typeinfo

def Event(payload):
    payload.field = 'Celsius'
    if payload.unit != '0':
        return False 
    payload.value = int(payload.data, 0) / 10
    return payload
