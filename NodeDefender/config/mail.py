from . import parser, configpath

def enabled():
    return True if parser['MAIL']['ENABLED'] == 'True' else False

def server():
    return parser['MAIL']['SERVER']

def port():
    return parser['MAIL']['PORT']

def tls():
    return True if parser['MAIL']['TLS'] == 'True' else False

def ssl():
    return True if parser['MAIL']['SSL'] == 'True' else False

def username():
    return parser['MAIL']['USERNAME']

def password():
    return parser['MAIL']['PASSWORD']

def get_cfg(key):
    return parser['MAIL'][key]

def set_cfg(**kwargs):
    for key, value in kwargs.items():
        parser['MAIL'][key] = str(value)

    with open(configpath, 'w') as fw:
        parser.write(fw)
