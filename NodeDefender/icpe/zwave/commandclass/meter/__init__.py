from NodeDefender.icpe.zwave.commandclass.meter import Electric

mtype = {'1' : 'Electric'}

def info(classtype = None):
    if classtype:
        try:
            return eval(mtype[classtype] + '.info')()
        except KeyError:
            return False
    return {'number' : '25',
            'name' : 'meter',
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
