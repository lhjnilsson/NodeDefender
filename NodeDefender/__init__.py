'''
Copyright (c) 2016 Connection Technology Systems Northern Europe

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE
SOFTWARE.
'''
from flask import Flask
import flask_login as login_manager
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO
from . import chconf
import logging
from queue import Queue
from apscheduler.schedulers.gevent import GeventScheduler
from gevent import monkey, sleep
monkey.patch_all()

# Setup logging
handler = logging.FileHandler('app.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# Initialize the Flask- Application
app = Flask(__name__)
app.config.from_object('config')

# Initialize Api
api = Api(app)

# Config-file 

# Initialize SocketIO
socketio = SocketIO(app)

# Initialize SQLAlchemy for Database
db = SQLAlchemy(app)
logger.info('Database started')


# For the Authentication
LoginMan = login_manager.LoginManager()
LoginMan.init_app(app)
LoginMan.login_view = 'login'
LoginMan.login_message_category = "info"

# Bcrypt for password- management
bcrypt = Bcrypt(app)

# Report that startup is successfull
logger.info('NodeDefender Succesfully started')

# Internal Message Queues
inMQTTQueue = Queue()
outMQTTQueue = Queue()

# Internal Socket Queues
outSocketQueue = Queue()

# Logging Queue
NodeLogQueue = Queue()


'''
below is temporary solution, to prevent from not starting
'''
MQTTConf = {key: value for (key, value) in chconf.ReadConf('MQTT1')}

try: # To make flask-script and DB init work if not present
    from . import models
    from .iCPE import iCPE
    from .mqtt import MQTT

    icpe = iCPE.iCPEset.FromDB()
    mqtt = MQTT(MQTTConf['ip'], MQTTConf['port'], icpe)

    from . import views, forms, sockets, mylogger, cronjobs
except Exception as e:
    print('Warning: Not able to start application, is Database updated?')
    print('Msg: ', e)

# Scheduled tasks
from . import cronjobs
StatTaskSched = GeventScheduler()
StatTaskSched.add_job(cronjobs.StatTask, 'interval', minutes=15)
HourlyCron = GeventScheduler()
HourlyCron.add_job(cronjobs.UpdateHourly, 'cron', hour='*')
DailyCron = GeventScheduler()
DailyCron.add_job(cronjobs.UpdateDaily, 'cron', day='*')

StatTaskSched.start()
HourlyCron.start()
DailyCron.start()
