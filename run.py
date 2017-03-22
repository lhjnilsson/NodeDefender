#!./py/bin/python
from NodeDefender import app, db
from NodeDefender import socketio
from NodeDefender.conn.mqtt import Load as LoadMQTT
from NodeDefender.iCPE import Load as LoadiCPE

if app.config['TESTING']:
    db.create_all()

LoadiCPE()
LoadMQTT()

socketio.run(app, host='0.0.0.0')
