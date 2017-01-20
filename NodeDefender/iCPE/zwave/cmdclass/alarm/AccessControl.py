

def Event(**kwargs):
    if kwargs['evt'] == '16':
        return {'door' : 'open'}
    elif kwargs['evt'] == '17':
        return {'door' : 'closed'}

def Load():
    return {}

def Form():
    pass
