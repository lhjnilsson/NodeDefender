icons = {True : 'fa fa-toggle-on', False : 'fa fa-toggle-off'}

info = {'name' : 'basic', 'number' : '20', 'types' : False}

field = {'type' : bool, 'readonly' : True, 'name' : 'Basic'}

def icon(value):
    return icons[eval(value)]

def event(payload):
    data = {'field' : field, 'info' : info}
    data['value'] = int(payload['value'], 16)
    data['state'] = True if payload['value'] else False
    data['icon'] = icons[data['state']]
    return data
