from flask_socketio import SocketIO, join_room
from .. import app

socketio = SocketIO(message_queue='redis://localhost:6379/0')

def FieldEvent(macaddr, sensorid, cmdclass, event):
    socketio.emit('FieldEvent', {'sensorid' : sensorid,
                                 'field' : cmdclass,
                                'event' : event},
                  namespace = '/icpe'+macaddr,
                  broadcast=True);
    print('evnent {}'.format(macaddr));
    return True
