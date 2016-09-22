#!./py/bin/python
from NodeDefender import app
from NodeDefender import socketio

socketio.run(app, debug=False, host='0.0.0.0')
