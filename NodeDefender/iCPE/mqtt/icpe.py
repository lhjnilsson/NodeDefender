from .import msg, Fire
from ...models.manage import mqtt as MQTTSQL

def SensorList(mac):
    i = iCPESQL.get(mac)
    if i is None:
        raise LookupError('Not able to find iCPE')

    if i.mqtt is None:
        raise ValueError('iCPE does not have any MQTT')

    return True

def Network(mac):
    pass

def Include(mac):
    pass

def SensorList(mac):
    m = MQTTSQL(mac)
    Fire(m.ipaddr, m.port, msg.format(mac, '0', 'act', 'list'))
    return True
