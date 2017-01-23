#!./py/bin/python
from NodeDefender import app
from NodeDefender import socketio
from NodeDefender.conn.mqtt import Load as LoadMQTT
from NodeDefender.iCPE import Load as LoadiCPE

LoadiCPE()
LoadMQTT()

socketio.run(app, debug=False, host='0.0.0.0')
