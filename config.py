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

CELERY_BROKER_URL = config['CELERY']['CELERY_BROKER_URL']
CELERY_RESULT_BACKEND = config['CELERY']['CELERY_RESULT_BACKEND']

SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
SECURITY_TRACKABLE = True
SECURITY_PASSWORD_SALT = 'something_super_secret_change_in_production'
