from NodeDefender.icpe.zwave.commandclass.meter import Electric

classtypes = {'1' : 'Electric'}
info = {'number' : '25', 'name' : 'meter', 'types' : True}
fields = None

def icon(value):
    return None

def event(payload):
    try:
        return eval(mtype[payload['mtype']] + '.event')(payload)
    except KeyError as e:
        print(str(e))
