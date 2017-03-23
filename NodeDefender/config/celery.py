from . import parser

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


def setup():
    print("Setting up Celery Configuration")
    
    broker = ''
    while not broker:
        broker = input("Enter Broker type:")

    server = ''
    while not server:
        server = input("Enter Server Address:")

    port = ''
    while not port:
        port = input("Enter Server Port:")

    database = ''
    while not database:
        database = input("Please Enter Database:")

    set({'ENABLED' : True,
         'BROKER' : broker,
         'SERVER' : server,
         'PORT' : port,
         'DATABASE' : database})
    
    return True

def get(key):
    return parser['CELERY'][key.upper()]

def set(**kwargs):
    for key, value in kwargs.items():
        parser['CELERY'][key] = value

    with open(configpath, 'w') as fw:
        parser.write(fw)
