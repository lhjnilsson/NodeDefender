from flask_socketio import SocketIO, join_room
from .. import app
from ..models.redis import sensor as SensorRedis
from ..models.redis import field as FieldRedis


socketio = SocketIO(message_queue='redis://localhost:6379/0')

def FieldEvent(event):
    socketio.emit('FieldEvent', (event.to_json()),
                  namespace = '/icpe'+event.icpe.macaddr,
                  broadcast=True);
    return True
