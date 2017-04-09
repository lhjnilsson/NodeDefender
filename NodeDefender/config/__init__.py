import os
from configparser import ConfigParser

parser = ConfigParser()
configpath = 'NodeDefender.conf'
parser.read(configpath)

basepath = os.path.abspath(os.path.dirname('..'))

from . import general as general_config
from . import database as database_config
from . import mail as mail_config
from . import logging as logging_config
from . import celery as celery_config

class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = general_config.secret_key()
    SECRET_SALT = general_config.secret_salt()
    SERVER_NAME = '127.0.0.1:5000'
    PORT = 5000
    WTF_CSRF_ENABLED = False
class ProductionConfig(Config):
    DATABASE = database_config.enabled()
    if DATABASE:
        DATABASE_ENGINE = database_config.engine()
        SQLALCHEMY_DATABASE_URI = database_config.uri()

    LOGGING = logging_config.enabled()
    if LOGGING:
        LOGGING_TYPE = logging_config.type()
        if LOGGING_TYPE == 'LOCAL':
            LOGGING_NAME = logging_config.name()
        if LOGGING_TYPE == 'SYSLOG':
            LOGGING_SERVER = logging_config.server()
            LOGGING_PORT = logging_config.port()


    MAIL = mail_config.enabled()
    if MAIL:
        MAIL_SERVER = mail_config.server()
        MAIL_PORT = mail_config.port()
        MAIL_USE_TLS = mail_config.tls()
        MAIL_USE_SSL = mail_config.ssl()
        MAIL_USERNAME = mail_config.username()
        MAIL_PASSWORD = mail_config.password()

    CELERY = celery_config.enabled()
    if CELERY:
        CELERY_BROKER = celery_config.broker()
        CELERY_BROKER_URI = celery_config.broker_uri()
        CELERY_BACKEND_URI = celery_config.backend_uri()

class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE = database_config.enabled()
    if DATABASE:
        DATABASE_ENGINE = database_config.engine()
        SQLALCHEMY_DATABASE_URI = database_config.uri()

    LOGGING = logging_config.enabled()
    if LOGGING:
        LOGGING_TYPE = logging_config.type()
        if LOGGING_TYPE == 'LOCAL':
            LOGGING_NAME = logging_config.name()
        if LOGGING_TYPE == 'SYSLOG':
            LOGGING_SERVER = logging_config.server()
            LOGGING_PORT = logging_config.port()


    MAIL = mail_config.enabled()
    if MAIL:
        MAIL_SERVER = mail_config.server()
        MAIL_PORT = mail_config.port()
        MAIL_USE_TLS = mail_config.tls()
        MAIL_USE_SSL = mail_config.ssl()
        MAIL_USERNAME = mail_config.username()
        MAIL_PASSWORD = mail_config.password()

    CELERY = celery_config.enabled()
    if CELERY:
        CELERY_BROKER = celery_config.broker()
        CELERY_BROKER_URI = celery_config.broker_uri()
        CELERY_BACKEND_URI = celery_config.backend_uri()



class TestingConfig(Config):
    TESTING = True
    pass
