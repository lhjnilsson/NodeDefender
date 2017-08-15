from NodeDefender.icpe.zwave.commandclass.alarm import AccessControl

classtypes = {'06' : 'AccessControl'}

def event(topic, payload):
    try:
        return eval(classtypes[payload['zalm']] + '.event')(topic, payload)
    except NameError:
        return False

def number():
    return 71

def classtype(typenumber):
    try:
        return classtypes[str(typenumber)]
    except KeyError:
        return False

def info(classtype):
    if classtype:
        try:
            return eval(types[classtype] + '.info')
        except (KeyError, NameError):
            return False
    return {'number' : '71',
            'name' : 'alarm',
            'types' : True}

def icon(value):
    return None

def web_field():
    return None
