from . import parser, configpath

def enabled():
    return parser['MAIL']['ENABLED']

def server():
    return parser['MAIL']['SERVER']

def port():
    return parser['MAIL']['PORT']

def tls():
    return parser['MAIL']['TLS']

def ssl():
    return parser['MAIL']['SSL']

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
