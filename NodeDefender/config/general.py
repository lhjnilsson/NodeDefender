from . import parser, configpath
from datetime import datetime

def hostname():
    return os.uname().nodename

def uptime():
    return str(datetime.now() - _loaded_at)

def secret_key():
    return parser['GENERAL']['KEY']

def secret_salt():
    return parser['GENERAL']['SALT']

def get_cfg(key):
    return parser['GENERAL'][key]

def set_cfg(**kwargs):
    for key, value in kwargs.items():
        parser['GENERAL'][key] = str(value)

    with open(configpath, 'w') as fw:
        parser.write(fw)