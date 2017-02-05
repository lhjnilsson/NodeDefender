def Info():
    return 'basic', False, {'type' : 'checkbox', 'readonly' : False, 'name' :
                            'Basic'}

def Load(classtypes):
    return {'basic' : None}

def Event(**kwargs):
    if kwargs['value'] == '0x00':
        return {'state' : 'off'}
    else:
        return {'state' : 'on'}
