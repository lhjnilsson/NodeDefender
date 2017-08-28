fields =  {'type' : 'value', 'readonly' : True, 'name' : 'Celsius'}
info = {'number' : '1', 'name' : 'AirTemperature', 'commandclass' : 'msensor'}

def event(payload):
    data = {'fields' : fields, 'info' : info}
    data['value'] = int(payload['data'], 0) / 10
    data['state'] = True if data['value'] else False
    data['icon'] = 'fa fa-thermometer-half'
    return payload

def icon(value):
    return 'fa fa-thermometer-half'
