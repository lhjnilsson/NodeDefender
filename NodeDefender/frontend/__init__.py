import NodeDefender.frontend.views
import NodeDefender.frontend.sockets

def load(app, socketio):
    NodeDefender.frontend.views.load_views(app)
    NodeDefender.frontend.sockets.load_sockets(socketio)
    return True

