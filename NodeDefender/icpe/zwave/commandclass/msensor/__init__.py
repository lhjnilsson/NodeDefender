from NodeDefender.icpe.zwave.commandclass.msensor import AirTemperature

mtype = {'1' : 'AirTemperature', '0x01' : 'AirTemperature',
         '01' : 'AirTemperature'}

def info(classtype = None):
    if classtype:
        try:
            return eval(mtype[classtype] + '.info')()
        except KeyError:
            return False
    return {'number' : '31',
            'name' : 'msensor',
            'types' : True}

def icon(value):
    return False

def load(classtypes):
    return {'meter' : 0}

def fields():
    return False

def event(payload):
    try:
        return eval(mtype[payload.type] + '.Event')(payload)
    except KeyError as e:
        print(str(e))
