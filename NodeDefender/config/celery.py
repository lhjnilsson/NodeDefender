import NodeDefender

config = {'enabled' : False}
default_config = {'enabled' : False,
                  'broker' : '',
                  'host' : '',
                  'port' : '',
                  'database' : ''}

def load_config(parser):
    config['enabled'] = eval(paser['CELERY']['ENABLED'])
    config['broker'] = parser['CELERY']['BROKER']
    config['host'] = parser['CELERY']['HOST']
    config['port'] = parser['CELERY']['PORT']
    config['database'] = parser['CELERY']['DATABASE']
 
def enabled():
    return config['enabled']

def broker():
    return config['broker']

def server():
    return config['host']

def port():
    return config['port']

def database():
    return config['database']

def broker_uri():
    if broker() == 'REDIS':
        return 'redis://'+server()+':'+port()+'/'+database()
    elif broker() == 'AMQP':
        return 'pyamqp://'+server()+':'+port()+'/'+database()
    else:
        return None

def set_defaults():
    for key, value in default_config.items():
        NodeDefender.config.parser['CELERY'][key] = str(value)
    return True

def set_config(**kwargs):
    for key, value in kwargs.items():
        NodeDefender.config.parser['CELERY'][key] = str(value)

    return NodeDefender.config.write()
