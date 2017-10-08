import NodeDefender

fields =  {'type' : 'value', 'readonly' : True, 'name' : 'Celsius', 'web_field'
           : True}
info = {'number' : '1', 'name' : 'AirTemperature', 'commandclass' : 'msensor'}

def event(payload):
    data = {'commandclass' : NodeDefender.icpe.zwave.commandclass.meter.info,
            'commandclasstype' : info, 'fields' : fields}
    data['value'] = int(payload['data'], 0) / 10
    data['state'] = True if data['value'] else False
    data['icon'] = 'fa fa-thermometer-half'
    return payload

def icon(value):
    return 'fa fa-thermometer-half'
