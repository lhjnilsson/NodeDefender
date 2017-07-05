from flask_script import Manager, prompt
from .. import config
from ..config import basepath

manager = Manager(usage="Setup NodeDefender Configuration")

def get_chunks(message):
    return [ message[i:i+38] for i in range(0, len(message), 38)]

def print_message(message):
    print("#")
    if len(message) > 38:
        for chunk in get_chunks(message):
            print("#" +  chunk.center(38))
    else:
        print("#" + message.center(38))
    print("#")
    return True

def print_topic(topic):
    print("****************************************")
    print("*" + topic.center(38) + "*")
    print("****************************************")
    return True

@manager.command
def database():
    print_topic('Database')
    engine = ""
    while not engine:
        engine = prompt("Enter DB Engine(SQLITE, MySQL)").lower()
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

    print("Storing database- settings...")
    config.database.set_cfg(**{'ENABLED' : True,
         'ENGINE' : engine,
         'SERVER' : server,
         'PORT' : port,
         'USERNAME' : username,
         'PASSWORD' : password,
         'DB' : db,
         'FILE_PATH' : filepath})
    print("Database- settings stored successful!")
    return True

@manager.command
def celery():
    print_topic("Celery")
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
        server = prompt("Enter Server Address")

    port = ''
    while not port:
        port = prompt("Enter Server Port")

    database = ''
    while not database:
        database = prompt("Enter Database")

    print("Storing celery- settings..")
    config.celery.set_cfg(**{'ENABLED' : True,
         'BROKER' : broker,
         'SERVER' : server,
         'PORT' : port,
         'DATABASE' : database})
    print("Celery- settings stored successful!")
    return True

@manager.command
def general():
    print_topic("General configuration")
    print("Server Name. If you are using a local running server please enter\
          as format NAME:PORT, e.g. 127.0.0.1:5000. Otherwise it will be\
          generating non- accessable URLs")
    servername = ""
    while not servername:
        servername = prompt("Enter Server Name")

    port = ""
    while not port:
        port = prompt("Which port should the server be running on")
    
    print("Security Key is used to Encrypt Password etc.")
    key = ""
    while not key:
        key = prompt("Enter Secret Key")

    print("Salt is used to genereate URLS and more.")
    salt = ""

    while not salt:
        salt = prompt("Please enter Salt")

    print("Storing general- settings..")
    config.general.set_cfg(**{'KEY' : key,
                                'SALT' : salt,
                                'SERVERNAME' : servername,
                                'PORT' : port})
    print("Successfully stored General Settings!")
    return True

@manager.command
def logging():
    print_topic("Logging")
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

    print("Storing Logging- settings..")
    config.logging.set_cfg(**{'ENABLED' : True,
         'TYPE' : loggtype,
         'NAME' : filepath,
         'SERVER' : server,
         'PORT' : port})
    print("Successfully stored logging settings");
    return True
 

@manager.command
def mail():
    print_topic("Mail")
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

    print("Saving mail- configuration")
    config.mail.set_cfg(**{'ENABLED' : True,
         'SERVER' : server,
         'PORT' : port,
         'TLS' : tls,
         'SSL' : ssl,
         'username' : username,
         'password' : password})
    print("Successfully stored Mail- configuration")
    return True

@manager.command
def all():
    general()
    database()
    mail()
    logging()
    celery()
    print_topic("Configuration Successfully stored!")
    print("Dont forget to migrate and upgrade the database before running")
    print("./manage.py db migrate")
    print("./manage.py db upgrade")
