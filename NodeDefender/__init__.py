from flask import Flask
from flask_socketio import SocketIO
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os
from datetime import datetime

import NodeDefender.config
import NodeDefender.factory
import NodeDefender.decorators
import NodeDefender.db
import NodeDefender.mqtt
import NodeDefender.icpe
import NodeDefender.mail
import NodeDefender.frontend

import gevent.monkey
gevent.monkey.patch_all()

hostname = os.uname().nodename
release = 'Alpha-2'
date_loaded = datetime.now()

app = None
socketio = None
celery = None
logger = None
loggHandler = None
login_manager = None
bcrypt = None
serializer = None

def create_app():
    global app
    global socketio
    global celery
    global logger
    global loggHandler
    global login_manger
    global bcrypt
    global serializer

    NodeDefender.config.load()

    app = CreateApp()
    logger, loggHandler = CreateLogging(app)

    try:
        socketio = SocketIO(app, message_queue=app.config['CELERY_BROKER_URI'],
                        async_mode='gevent')
    except KeyError:
        socketio = SocketIO(app, async_mode='gevent')

    celery = CreateCelery(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth_view.authenticate'
    login_manager.login_message_category = "info"

    bcrypt = Bcrypt(app)

    serializer = Serializer(app)
    
    try:
        NodeDefender.db.load(app, loggHandler)
        NodeDefender.frontend.load(app, socketio)
        NodeDefender.mqtt.load(loggHandler)
        NodeDefender.icpe.load(loggHandler)
    except Exception as e:
        logger.critical("Unable to load NodeDefender")
        return None

    logger.info('NodeDefender Succesfully started')
    return app

