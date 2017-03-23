from . import parser

def enabled():
    return parser['DATABASE']['ENABLED']

def engine():
    return parser['DATABASE']['ENGINE']

def username():
    return parser['DATABASE']['USERNAME']

def password():
    return parser['DATABASE']['PASSWORD']

def server():
    return parser['DATABASE']['SERVER']

def port():
    return parser['DATABASE']['PORT']

def db():
    return parser['DATABASE']['DB']

def mysql_uri():
    return 'mysql://'+username()+':'+password()+'@'+server()+':'+port()+'/'+db()

def postgres_uri():
    return 'postgresql://'+username()+':'+password()+'@'\
            +sever()+':'+port()+'/'+db()

def sqlite_uri():
    return 'sqlite:///' + parser['DATABASE']['FILE_PATH']

def uri():
    db_engine = engine()
    return eval(db_engine + '_uri')()

def setup():
    print("Setting up Database Configuration")
    
    engine = ""
    while not engine:
        engine = input("Enter DB Engine(SQLITE, MYSQL, PosgreSQL):")
        if engine == 'sqlite':
            server = 'Not Used'
            port = 'Not Used'
            username = 'Not Used'
            password = 'Not Used'
            db = 'Not Used'
            filepath = ''
        elif engine == 'mysql':
            server = ''
            port = ''
            username = ''
            password = ''
            db = ''
            filepath = 'Not Used'
        elif engine == 'postgresql':
            server = ''
            port = ''
            username = ''
            password = ''
            db = ''
            filepath = 'Not Used'
        else:
            engine = ''

    while not server:
        server = input('Enter Server Address:')

    while not port:
        port = input('Enter Server Port:')

    while not username:
        username = input('Enter Username:')

    while not password:
        password = input('Enter Password:')

    while not db:
        db = input("Enter DB Name/Number:")

    while not filepath:
        filepath = input("Enter File Path:")

    set({'ENABLED' : True,
         'ENGINE' : engine,
         'SERVER' : server,
         'PORT' : port,
         'USERNAME' : username,
         'PASSWORD' : password,
         'DB' : db,
         'FILE_PATH' : filepath})

    return True

def get(key):
    return parser['DATABASE'][key]

def set(**kwargs):
    for key, value in kwargs.items():
        parser['DATABASE'][key] = value

    with open(configpath, 'w') as fw:
        parser.write(fw)
