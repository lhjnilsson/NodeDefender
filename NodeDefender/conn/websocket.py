from flask_socketio import SocketIO, join_room
from .. import app
from ..models.redis import sensor as SensorRedis
from ..models.redis import field as FieldRedis


socketio = SocketIO(message_queue='redis://localhost:6379/0')

def ZWaveEvent(event):
    if 'icpe' not in event:
        return False

    socketio.emit('ZWaveEvent', (event),
                  namespace = '/icpe'+event['icpe'],
                  broadcast=True);
    return True
