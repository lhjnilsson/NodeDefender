import NodeDefender

config = {'enabled' : False}
default_config = {'enabled' : False,
                  'engine' : '',
                  'username' : '',
                  'password' : '',
                  'host' : '',
                  'port' : '',
                  'database' : '',
                  'filepath' : ''}

def load_config(parser):
    config['enabled'] = eval(parser['DATABASE']['ENABLED'])
    config['engine'] = parser['DATABASE']['ENGINE']
    config['username'] = parser['DATABASE']['USERNAME']
    config['password'] = parser['DATABASE']['PASSWORD']
    config['host'] = parser['DATABASE']['HOST']
    config['port'] = parser['DATABASE']['PORT']
    config['database'] = parser['DATABASE']['DATABASE']
    config['filepath'] = parser['DATABASE']['FILEPATH']
    return config

def enabled():
    return config['enabled']

def engine():
    return config['engine']

def username():
    return config['username']

def password():
    return config['password']

def host():
    return config['host']

def port():
    return config['port']

def database():
    return config['database']

def filepath():
    return config['filepath']

def mysql_uri():
    return 'mysql+pymysql://'+username()+':'+password()+'@'+host()+':'+port()\
            +'/'+database()

def postgresql_uri():
    return 'postgresql://'+username()+':'+password()+'@'\
            +host()+':'+port()+'/'+database()

def sqlite_uri():
    return 'sqlite:///' + filepath()

def uri():
    db_engine = engine()
    return eval(db_engine + '_uri')()

def set_defaults():
    for key, value in default_config.items():
        NodeDefender.config.parser['DATABASE'][key] = str(value)
    return True

def set_config(**kwargs):
    for key, value in kwargs.items():
        NodeDefender.config.parser['DATABASE'][key] = str(value)

    return NodeDefender.config.write()
