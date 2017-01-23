def Info():
    return 'basic', False

def Load(classtypes):
    return {'basic' : None}

def Event(**kwargs):
    if kwargs['value'] == '0x00':
        return {'state' : 'off'}
    else:
        return {'state' : 'on'}
