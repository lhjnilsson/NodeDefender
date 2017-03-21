from . import parser
from datetime import datetime

def hostname():
    return os.uname().nodename

def uptime():
    return str(datetime.now() - _loaded_at)

def secret_key():
    return parser['GENERAL']['KEY']

def secret_salt():
    return parser['GENERAL']['SALT']
