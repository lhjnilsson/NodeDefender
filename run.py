#!./py/bin/python
import NodeDefender

app = NodeDefender.create_app()

NodeDefender.socketio.run(app)
