from flask_socketio import SocketIO, join_room
from .. import app

socketio = SocketIO(message_queue='redis://localhost:6379/0')

def CmdclassEvent(macaddr, sensorid, cmdclass, event):
    socketio.emit('CmdclassEvent', {'macaddr' : macaddr, 
                                    'sensorid' : sensorid,
                                    'cmdclass' : cmdclass,
                                    'event' : event},
                  namespace = '/icpe'+macaddr,
                  broadcast=True);
    print('evnent {}'.format(macaddr));
    return True
