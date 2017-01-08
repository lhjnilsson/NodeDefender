from . import msg, Fire
from ...models.manage import mqtt as MQTTSQL

def Query(mac, sensorid, mqtt = None):
    return Fire(mqtt.ipaddr, mqtt.port, msg.format(mac, sensorid, 'node', 'qry'))
