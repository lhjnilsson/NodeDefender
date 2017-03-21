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
    return 'NodeDefender.db'

def uri():
    db_engine = engine()
    return eval(db_engine + '_uri')()
