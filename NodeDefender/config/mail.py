from . import parser

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

def setup():
    print("Setting up Mail Configuration")
    
    server = ''
    while not server:
        server = input("Enter Server Address:")

    port = ''
    while not port:
        port = input("Enter Server Port:")

    tls = ''
    while type(tls) is str:
        tls = input("TLS Enabled(Y/N)?")
        if tls[1].upper() == 'Y':
            tls = True
        if tls[1].upper() == 'N':
            tls = False

    ssl = ''
    while type(ssl) is str:
        ssl = input("TLS Enabled(Y/N)?")
        if ssl[1].upper() == 'Y':
            ssl = True
        if ssl[1].upper() == 'N':
            ssl = False

    username = ''
    while not username:
        username = input('Username:')

    password = ''
    while not password:
        password = input('Password')

    set({'ENABLED' : True,
         'SERVER' : server,
         'PORT' : port,
         'TLS' : tls,
         'SSL' : ssl,
         'username' : username,
         'password' : password})

    return True
def get(key):
    return parser['GENERAL'][key]

def set(**kwargs):
    for key, value in kwargs.items():
        parser['GENERAL'][key] = value

    with open(configpath, 'w') as fw:
        parser.write(fw)
