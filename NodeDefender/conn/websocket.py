from flask_socketio import SocketIO, join_room
from .. import app
from ..models.redis import sensor as SensorRedis
from ..models.redis import field as FieldRedis


socketio = SocketIO(message_queue='redis://localhost:6379/0')

def FieldEvent(macaddr, sensorid, field, event):
    sensor = SensorRedis.Get(macaddr, sensorid)
    field = FieldRedis.Get(macaddr, sensorid, field)
    
    socketio.emit('FieldEvent', (sensor, field, event),
                  namespace = '/icpe'+macaddr,
                  broadcast=True);
    return True
