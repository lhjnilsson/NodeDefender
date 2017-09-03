import logging
from flask import Flask
from flask_moment import Moment
from celery import Celery
from itsdangerous import URLSafeSerializer
from flask_wtf.csrf import CSRFProtect
from NodeDefender import config
import os

csfr = CSRFProtect()
moment = Moment()

def CreateApp():
    app = Flask(__name__)
    try:
        mode = os.environ['NodeDefender_Mode']
        pass
    except KeyError:
        print('NodeDefender_Mode not set, running as Production.')
        mode = 'Production'
        
    app.config.from_object('NodeDefender.config.'+mode+'Config')
    app.template_folder = "templates"
    app.static_folder = "templates/frontend/static"
    moment.init_app(app)
    return app

def CreateLogging(app = None):
    app = app or CreateApp()
    try:
        if app.config['LOGGING_TYPE'] == 'LOCAL':
            loggHandler = logging.FileHandler(app.config['LOGGING_NAME'])
        elif app.config['LOGGING_TYPE'] == 'SYSLOG':
            loggHandler = logging.handlers.SysLogHandler(address = (app.config['LOGGING_SERVER'],
                                                  int(app.config['LOGGING_PORT'])))
    except KeyError:
        loggHandler = logging.StreamHandler()
    
    loggHandler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    loggHandler.setFormatter(formatter)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(loggHandler)
    return logger, loggHandler

def CreateCelery(app = None):
    app = app or CreateApp()
    try:
        celery = Celery(app.name, broker=app.config['CELERY_BROKER_URI'],
                   backend=app.config['CELERY_BACKEND_URI'])
    except KeyError:
        print('Celery Configuration incomplete. Concurreny disabled')
        celery = Celery(app.name)
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

class Serializer:
    def __init__(self, app):
        self.serializer = URLSafeSerializer(app.config['SECRET_KEY'])
        self.salt = app.config['SECRET_SALT']

    def loads(self, token):
        return self.serializer.loads(token)

    def dumps(self, string):
        return self.serializer.dumps(string)

    def loads_salted(self, token):
        return self.serializer.loads(token, salt=self.salt)

    def dumps_salted(self, string):
        return self.serializer.dumps(string, salt=self.salt)
