fields = {'type' : 'value', 'readonly' : True, 'name' : 'Watt'}

info = {'name' : 'Electric', 'number' : '01', 'commandclass' : 'meter'}

def icon(value):
    return 'fa fa-plug'

def event(payload):
    data = {'field' : fields, 'info' : info}
    data['value'] = int(payload['data32'], 0) / 10
    data['state'] = True if data['value'] > 1.0 else False
    data['icon'] = 'fa fa-plug'
    return payload
