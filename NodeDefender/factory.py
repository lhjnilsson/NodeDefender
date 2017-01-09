import logging
from flask import Flask
from celery import Celery

def CreateApp():
    app = Flask(__name__)
    app.config.from_object('config')
    app.template_folder = "frontend/templates"
    app.static_folder = "frontend/static"
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
