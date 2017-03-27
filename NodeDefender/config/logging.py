from . import parser, configpath

def enabled():
    return True if parser['LOGGING']['ENABLED'] == 'True' else False

def type():
    return parser['LOGGING']['TYPE']

def name():
    return parser['LOGGING']['NAME']

def server():
    return parser['LOGGING']['SERVER']

def port():
    return parser['LOGGING']['PORT']

def get_cfg(key):
    return parser['LOGGING'][key]

def set_cfg(**kwargs):
    for key, value in kwargs.items():
        parser['LOGGING'][key] = str(value)

    with open(configpath, 'w') as fw:
        parser.write(fw)
