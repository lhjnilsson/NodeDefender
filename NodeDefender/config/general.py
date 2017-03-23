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

def setup():
    print("Setting up General Configuration")
    key = ""
    
    while not key:
        key = input("Enter Secret Key:")

    salt = ""

    while not salt:
        salt = input("Please enter Salt:")

def get(key):
    return parser['GENERAL'][key]

def set(**kwargs):
    for key, value in kwargs.items():
        parser['GENERAL'][key] = value

    with open(configpath, 'w') as fw:
        parser.write(fw)
