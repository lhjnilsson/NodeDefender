def Event(**kwargs):
    return {'Watt' : int(kwargs['data'], 0) / 10}
