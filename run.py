#!./py/bin/python
from NodeDefender import app, db
from NodeDefender import socketio
from NodeDefender.conn.mqtt import Load as LoadMQTT

if app.config['TESTING']:
    db.create_all()

LoadMQTT()

socketio.run(app, host='0.0.0.0')
