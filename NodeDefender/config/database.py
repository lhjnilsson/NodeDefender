from . import parser, configpath

def enabled():
    return True if parser['DATABASE']['ENABLED'] == 'True' else False

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

def file():
    return parser['DATABASE']['FILE_PATH']

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

def get_cfg(key):
    return parser['DATABASE'][key]

def set_cfg(**kwargs):
    for key, value in kwargs.items():
        parser['DATABASE'][key] = str(value)

    with open(configpath, 'w') as fw:
        parser.write(fw)
