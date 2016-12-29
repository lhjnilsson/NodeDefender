from . import mqtt
from ..models.SQL import MQTTModel

def LoadMQTT():
    for m in MQTTModel.query.all():
        mqtt.Add(m.ipaddr, m.port, m.username, m.password)
