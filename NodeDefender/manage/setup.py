from flask_script import Manager, prompt
from .. import config
from ..config import basepath

manager = Manager(usage="Setup NodeDefender Configuration")

@manager.command
def database():
    print('Setting up Database..')
    engine = ""
    while not engine:
        engine = prompt("Enter DB Engine(SQLITE, MYSQL, PosgreSQL)").lower()
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
            print('Not Recognized, please try again')
            engine = ''

    while not server:
        server = prompt('Enter Server Address')

    while not port:
        port = prompt('Enter Server Port')

    while not username:
        username = prompt('Enter Username')

    while not password:
        password = prompt('Enter Password')

    while not db:
        db = prompt("Enter DB Name/Number")

    while not filepath:
        print("FilePath for SQLite Database, Enter leading slash(/) for\
              absolute- path. Otherwise relative to your current folder.")
        filepath = prompt("Enter File Path")
    
    if filepath[0] == '/':
        filepath = filepath
    else:
        filepath = basepath + '/' + filepath

    config.database.set_cfg(**{'ENABLED' : True,
         'ENGINE' : engine,
         'SERVER' : server,
         'PORT' : port,
         'USERNAME' : username,
         'DB' : db,
         'FILE_PATH' : filepath})

    return True

@manager.command
def celery():
    print("Setting up Celery. Used for Currentent and required to have")
    broker = ''
    while not broker:
        broker = prompt("Enter Broker type(AMQP or Redis):")
        if broker.lower() == 'amqp':
            broker = 'AMQP'
        elif broker.lower() == 'redis':
            broker = 'REDIS'
        else:
            print("Unknown broker, please try again")
            broker = ''

    server = ''
    while not server:
        server = prompt("Enter Server Address:")

    port = ''
    while not port:
        port = prompt("Enter Server Port:")

    database = ''
    while not database:
        database = prompt("Please Enter Database:")

    config.celery.set_cfg(**{'ENABLED' : True,
         'BROKER' : broker,
         'SERVER' : server,
         'PORT' : port,
         'DATABASE' : database})
    
    return True

@manager.command
def general():
    print("Setting up General configuration.")
    print("Secret key is used for encryption, Salt is used for Hashing")
    key = ""
    
    while not key:
        key = prompt("Enter Secret Key:")

    salt = ""

    while not salt:
        salt = prompt("Please enter Salt:")

    config.general.set_cfg(**{'KEY' : key,
                           'SALT' : salt})
    return True

@manager.command
def logging():
    print("Logging used to get run-time information")
    loggtype = ""
    while not loggtype:
        loggtype = prompt("Enter Logging Type(Syslog/Local):").lower()
        if loggtype.lower() == 'syslog':
            loggtype = 'SYSLOG'
        elif loggtype.lower() == 'local':
            loggtype = 'LOCAL'
        else:
            print("Unknown loggtype, please try again")
            loggtype = ''

    filepath = ''
    server = ''
    port = ''
    level = ''

    if loggtype == 'LOCAL':
        server = 'Not set'
        port = 'Not set'
    
    if loggtype == 'SYSLOG':
        filepath = 'Not used'

    while not filepath:
        print("Enter filepath for loggingfile. Leading slah(/) for absolute-\
              path. Otherwise relative to current directory")
        filepath = prompt("Please Filename:")

    if filepath[0] == '/':
        filepath = filepath
    else:
        filepath = basepath + '/' + filepath

    while not server:
        server = prompt('Please enter Syslog IP')

    while not port:
        port = prompt('Please enter Syslog Port')

    config.logging.set_cfg(**{'ENABLED' : True,
         'TYPE' : loggtype,
         'NAME' : filepath,
         'SERVER' : server,
         'PORT' : port})
    
    return True
 

@manager.command
def mail():
    print("Setting up Mail configuration. Mail is used to add new users, \
          send notfications to groups and users and more..")
    server = ''
    while not server:
        server = prompt("Enter Server Address:")

    port = ''
    while not port:
        port = prompt("Enter Server Port:")

    tls = ''
    while type(tls) is str:
        tls = prompt("TLS Enabled(Y/N)?")
        if tls[0].upper() == 'Y':
            tls = True
        elif tls[0].upper() == 'N':
            tls = False
        else:
            tls = ''

    ssl = ''
    while type(ssl) is str:
        ssl = prompt("SSL Enabled(Y/N)?")
        if ssl[0].upper() == 'Y':
            ssl = True
        elif ssl[0].upper() == 'N':
            ssl = False
        else:
            ssl = ''

    username = ''
    while not username:
        username = prompt('Username:')

    password = ''
    while not password:
        password = prompt('Password')

    config.mail.set_cfg(**{'ENABLED' : True,
         'SERVER' : server,
         'PORT' : port,
         'TLS' : tls,
         'SSL' : ssl,
         'username' : username,
         'password' : password})

    return True

@manager.command
def all():
    general()
    database()
    mail()
    logging()
    celery()
