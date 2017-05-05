from flask_script import Manager, prompt
from .. import config
from ..config import basepath

manager = Manager(usage="Setup NodeDefender Configuration")

@manager.command
def database():
    print('\nSetting up Database..\n')
    engine = ""
    while not engine:
        engine = prompt("Enter DB Engine(SQLITE, MYSQL, PosgreSQL):").lower()
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
        server = prompt('\nEnter Server Address')

    while not port:
        port = prompt('\nEnter Server Port')

    while not username:
        username = prompt('\nEnter Username')

    while not password:
        password = prompt('\nEnter Password')

    while not db:
        db = prompt("\nEnter DB Name/Number")

    while not filepath:
        print("\nFilePath for SQLite Database, Enter leading slash(/) for\
              absolute- path. Otherwise relative to your current folder.")
        filepath = prompt("Enter File Path")
    
    if filepath[0] == '/':
        filepath = filepath
    else:
        filepath = basepath + '/' + filepath

    print("\nStoring database- settings...")
    config.database.set_cfg(**{'ENABLED' : True,
         'ENGINE' : engine,
         'SERVER' : server,
         'PORT' : port,
         'USERNAME' : username,
         'DB' : db,
         'FILE_PATH' : filepath})
    print("\nDatabase- settings stored successful!\n")
    return True

@manager.command
def celery():
    print("\nSetting up Celery. Used for Currentent and required to have\n")
    broker = ''
    while not broker:
        broker = prompt("Enter Broker type(AMQP or Redis)")
        if broker.lower() == 'amqp':
            broker = 'AMQP'
        elif broker.lower() == 'redis':
            broker = 'REDIS'
        else:
            print("Unknown broker, please try again")
            broker = ''

    server = ''
    while not server:
        server = prompt("\nEnter Server Address")

    port = ''
    while not port:
        port = prompt("\nEnter Server Port:")

    database = ''
    while not database:
        database = prompt("\nEnter Database:")

    print("\nStoring celery- settings..\n")
    config.celery.set_cfg(**{'ENABLED' : True,
         'BROKER' : broker,
         'SERVER' : server,
         'PORT' : port,
         'DATABASE' : database})
    print("\nCelery- settings stored successful!\n")
    return True

@manager.command
def general():
    print("Setting up General configuration.\n")
    print("Server Name. If you are using a local running server please enter\
          as format NAME:PORT, e.g. 127.0.0.1:5000. Otherwise it will be\
          generating non- accessable URLs")
    servername = ""
    while not servername:
        servername = prompt("Enter Server Name")

    port = ""
    while not port:
        port = prompt("\nWhich port should the server be running on:")
    
    print("\n\nSecurity Key is used to Encrypt Password etc.")
    key = ""
    while not key:
        key = prompt("Enter Secret Key")

    print("\nSalt is used to genereate URLS and more.")
    salt = ""

    while not salt:
        salt = prompt("Please enter Salt")

    print("\nStoring general- settings..\n")
    config.general.set_cfg(**{'KEY' : key,
                                'SALT' : salt,
                                'SERVERNAME' : servername,
                                'PORT' : port})
    print("\nSuccessfully stored General Settings!\n")
    return True

@manager.command
def logging():
    print("\nLogging used to get run-time information\n")
    loggtype = ""
    while not loggtype:
        loggtype = prompt("Enter Logging Type(Syslog/Local)").lower()
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
        filepath = prompt("Please Filename")

    if filepath[0] == '/':
        filepath = filepath
    else:
        filepath = basepath + '/' + filepath

    while not server:
        server = prompt('Enter Syslog IP')

    while not port:
        port = prompt('Enter Syslog Port')

    print("\nStoring Logging- settings..\n")
    config.logging.set_cfg(**{'ENABLED' : True,
         'TYPE' : loggtype,
         'NAME' : filepath,
         'SERVER' : server,
         'PORT' : port})
    print("\nSuccessfully stored logging settings\n");
    return True
 

@manager.command
def mail():
    print("Setting up Mail configuration. Mail is used to add new users, \
          send notfications to groups and users and more..")
    server = ''
    while not server:
        server = prompt("Enter Server Address")

    port = ''
    while not port:
        port = prompt("Enter Server Port")

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
        username = prompt('Username')

    password = ''
    while not password:
        password = prompt('Password')

    print("\nSetting mail- configuration\n")
    config.mail.set_cfg(**{'ENABLED' : True,
         'SERVER' : server,
         'PORT' : port,
         'TLS' : tls,
         'SSL' : ssl,
         'username' : username,
         'password' : password})
    print("\nSuccessfully stored Mail- configuration\n")
    return True

@manager.command
def all():
    general()
    database()
    mail()
    logging()
    celery()
