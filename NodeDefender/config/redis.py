import NodeDefender

config = {'enabled' : False}
default_config = {'enabled' : False,
                  'host' : '',
                  'port' : '',
                  'database' : ''}

def enabled():
    return config['enabled']

def host():
    return config['host']

def port():
    return config['port']

def database():
    return config['database']

def set_defaults():
    for key, value in default_config.items():
        NodeDefender.config.parser['REDIS'][key] = str(value)

def set_cfg(**kwargs):
    for key, value in kwargs.items():
        NodeDefender.config.parser['REDIS'][key] = str(value)

    return NodeDefender.config.write()
