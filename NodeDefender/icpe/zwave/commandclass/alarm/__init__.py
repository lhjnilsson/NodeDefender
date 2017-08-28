from NodeDefender.icpe.zwave.commandclass.alarm import AccessControl

classtypes = {'06' : 'AccessControl'}
info = {'number' : '71', 'name' : 'alarm', 'types' : True}
field = None

def event(payload):
    try:
        return eval(classtypes[payload['zalm']] + '.event')(payload)
    except NameError:
        print("Not found ")
        return False

def icon(value):
    return None
