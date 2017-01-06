from . import msg, Fire
from ...models.manage import mqtt as MQTTSQL

def Query(mac, sensorid):
    m = MQTTSQL.iCPE(mac)
    Fire(m.ipaddr, m.port, msg.format(mac, sensorid, 'node', 'list'))
    return True
