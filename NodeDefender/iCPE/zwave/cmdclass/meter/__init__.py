mtype = {'1' : 'Electric'}

def Load(classtypes):
    return {'meter' : 0}


def Event(**kwargs):
    try:
        return eval(mtype[kwargs['type']] + '.Event')(**kwargs)
    except NameError as e:
        print(kwargs['type'], e)

from . import Electric
