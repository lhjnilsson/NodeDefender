import NodeDefender

fields = {'type' : 'value', 'readonly' : True, 'name' : 'Watt',
          'web_field' : True}

info = {'name' : 'Electric', 'number' : '1', 'commandclass' : 'meter'}

def icon(value):
    return 'fa fa-plug'

def event(payload):
    data = {'commandclass' : NodeDefender.icpe.zwave.commandclass.meter.info,
            'commandclasstype' : info, 'fields' : fields}
    if data['unit'] == '0':
        precision = int("1" + ("0" * int(payload["precision"])))
        data['value'] = float.fromhex(payload["data"])
        data['value'] /= precision
    elif data['unit'] == '2':
        data['value'] = int(payload['data'], 0)
    data['state'] = True if data['value'] > 1.0 else False
    data['icon'] = 'fa fa-plug'
    return data
