from . import parser, configpath

def enabled():
    return parser['CELERY']['ENABLED']

def broker():
    return parser['CELERY']['BROKER']

def server():
    return parser['CELERY']['SERVER']

def port():
    return parser['CELERY']['PORT']

def database():
    return parser['CELERY']['DATABASE']

def broker_uri():
    if broker() == 'REDIS':
        return 'redis://'+server()+':'+port()+'/'+database()
    elif broker() == 'AMQP':
        return 'pyamqp://'+server()+':'+port()+'/'+database()
    else:
        return None

def backend_uri():
    if broker() == 'REDIS':
        return 'redis://'+server()+':'+port()+'/'+database()
    elif broker() == 'AMQP':
        return 'rpc://'+server()+':'+port()+'/'+database()
    else:
        return None

def get_cfg(key):
    return parser['CELERY'][key.upper()]

def set_cfg(**kwargs):
    for key, value in kwargs.items():
        parser['CELERY'][key] = str(value)

    with open(configpath, 'w') as fw:
        parser.write(fw)
