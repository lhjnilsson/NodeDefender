zalm = {'06' : 'AccessControl'}

def Load():
    return {'notification': None}

def Event(**kwargs):
    try:
        return eval(zalm[kwargs['zalm']] + '.Event')(**kwargs)
    except NameError as e:
        print(kwargs['zalm'], e)


from . import AccessControl
