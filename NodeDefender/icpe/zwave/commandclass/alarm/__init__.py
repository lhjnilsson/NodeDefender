from NodeDefender.icpe.zwave.commandclass.alarm import AccessControl

classtypes = {'06' : 'AccessControl'}
info = {'number' : '71', 'name' : 'alarm', 'types' : True}
field = None

def event(payload):
    return False

def icon(value):
    return None
