#!./py/bin/python
from NodeDefender import app, db
from NodeDefender import socketio
from NodeDefender.mqtt import connection
#from NodeDefender.iCPE.db import Load as LoadiCPE

if app.config['TESTING']:
    db.create_all()

#LoadiCPE()
connection.load()
db.load()

socketio.run(app, host='0.0.0.0')
