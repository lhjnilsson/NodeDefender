import NodeDefender

default_config = {'enabled' : False,
                  'engine' : '',
                  'username' : '',
                  'password' : '',
                  'host' : '',
                  'port' : '',
                  'database' : '',
                  'filepath' : ''}

config = default_config.copy()

def load_config(parser):
    config['enabled'] = eval(parser['DATABASE']['ENABLED'])
    config['engine'] = parser['DATABASE']['ENGINE']
    config['username'] = parser['DATABASE']['USERNAME']
    config['password'] = parser['DATABASE']['PASSWORD']
    config['host'] = parser['DATABASE']['HOST']
    config['port'] = parser['DATABASE']['PORT']
    config['database'] = parser['DATABASE']['DATABASE']
    config['filepath'] = parser['DATABASE']['FILEPATH']
    NodeDefender.app.config.update(
        DATABASE=config['enabled'],
        DATABASE_ENGINE=config['engine'],
        DATABASE_USERNAME=config['username'],
        DATABASE_PASSWORD=config['password'],
        DATABASE_HOST=config['host'],
        DATABASE_PORT=config['port'],
        DATABASE_DATABASE=config['database'],
        DATABASE_FILEPATH=config['filepath'])
    if NodeDefender.app.testing:
        NodeDefender.app.config.update(
            SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:")
    else:
        NodeDefender.app.config.update(
            SQLALCHEMY_DATABASE_URI = get_uri())
    return config

def get_uri():
    if config['engine'] == 'sqlite':
        return 'sqlite:///' + NodeDefender.config.parser['DATABASE']['FILEPATH']
    username = config['username']
    password = config['password']
    host = config['host']
    port = config['port']
    database = config['database']
    if config['engine'] == 'mysql':
        return 'mysql+pymysql://'+username+':'+password+'@'+host+':'+port+\
            '/'+database
    elif config['engine'] == 'postgresql':
        return 'postgresql://'+username+':'+password+'@'+host+':'+port+\
                '/'+database()
    return "sqlite:///:memory:"

def set_default():
    for key, value in default_config.items():
        NodeDefender.config.parser['DATABASE'][key] = str(value)
    return True

def set(**kwargs):
    for key, value in kwargs.items():
        if key not in config:
            continue
        NodeDefender.config.database.config['KEY'] = str(value)
    return True

def write():
    NodeDefender.config.parser['DATABASE'] = config
    NodeDefender.config.write()
