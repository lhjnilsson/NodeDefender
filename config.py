import os
from configparser import ConfigParser
config = ConfigParser()

config.read('settings.ini')

basedir = os.path.abspath(os.path.dirname(__file__))

if config['DATABASE']['SQL'] == 'local':
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, \
            config['LOCALSQL']['URI'])
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repo')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


SECRET_KEY = config['BASE']['key']
WTF_CSRF_ENABLED = True

