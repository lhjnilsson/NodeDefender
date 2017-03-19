import logging
from flask import Flask
from celery import Celery
from flask_moment import Moment
from itsdangerous import URLSafeSerializer
moment = Moment()

def CreateApp():
    app = Flask(__name__)
    app.config.from_object('config')
    app.template_folder = "frontend/templates"
    app.static_folder = "frontend/static"
    moment.init_app(app)
    return app

def CreateLogging():
    handler = logging.FileHandler('app.log')
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger, handler

def CreateCelery(app = None):
    app = app or CreateApp()
    celery = Celery(app.name, broker="redis://localhost:6379/0")
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
        return self.serializer.dumps(token, salt=self.salt)

