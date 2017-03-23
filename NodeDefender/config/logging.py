from . import parser

def enabled():
    return parser['LOGGING']['ENABLED']

def type():
    return parser['LOGGING']['TYPE']

def name():
    return parser['LOGGING']['NAME']

def server():
    return parser['LOGGING']['SERVER']

def port():
    return parser['LOGGING']['PORT']


def setup():
    print("Setting up Logging Configuration")
    loggtype = ""
    
    while not loggtype:
        loggtype = input("Enter Logging Type:").lower()
        if loggtype != 'syslog' or loggtype != 'local':
            loggtype = ''

    name = ''
    server = ''
    port = ''

    if loggtype == 'local':
        server = 'Not set'
        port = 'Not set'
    
    if loggtype == 'syslog':
        name = 'not used'

    while not name:
        name = input("Please Filename:")

    while not server:
        server = input('Please enter Syslog IP')

    while not port:
        port = input('Please enter Syslog Port')

    set({'ENABLED' : True,
         'TYPE' : loggtype,
         'NAME' : name,
         'SERVER' : server,
         'PORT' : port})

    return True

def get(key):
    return parser['LOGGING'][key]

def set(**kwargs):
    for key, value in kwargs.items():
        parser['LOGGING'][key] = value

    with open(configpath, 'w') as fw:
        parser.write(fw)
