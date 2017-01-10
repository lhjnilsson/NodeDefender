from ...models.manage import sensor as SensorSQL
from . import redisconn
from .. import mqtt, zwave
from datetime import datetime
'''
    For Sensor:
        {
        Node ID
        Unsupported
        Role Type
        Device Type
        cmdclass = {
            basic {
                e.g. Status: On
                e.g. Rules: False
            }
            msensor {
                e.g. Status: Open
                e.g. Rules: {

                }
            }
        ]
'''
@redisconn
def Create(mac, sensorid, conn):
    if SensorSQL.Get(mac, sensorid):
        raise ValueError('Already exists')
    return SensorSQL.Create(mac, sensorid)

@redisconn
def Get(mac, sensorid, conn):
    sensor = conn.hgetall(mac + sensorid)
    if len(sensor):
        return sensor
    else:
        return None

def CreateLoadQuery(mqttsrc, mac, sensorid):
    if Load(mac, sensorid) is not None:
        raise ValueError('Already exists')
    
    Create(mac, sensorid)
    Load(mac, sensorid)
    mqtt.sensor.Query(mac, sensorid, **mqttsrc)
    return True


@redisconn
def Load(mac, sensorid, conn):
    sensor = SensorSQL.Get(mac, sensorid)
    if sensor is None:
        return None
    supported, unsupported = zwave.Load([cmdclass for cmdclass in
                                         sensor.cmdclasses])
    s = {
        'name' : sensor.name,
        'sensorid' : sensor.sensorid,
        'roletype' : sensor.roletype,
        'devicetype' : sensor.devicetype,
        'unsupported' : unsupported,
        'cmdclass' : supported
    }

    conn.hmset(mac + sensorid, s)
    return s

@redisconn
def Save(mac, sensorid, conn, **kwargs):
    s = conn.hgetall(mac + sensorid)
    for key, value in kwargs:
        s[key] = value

    conn.hmset(mac + sensorid, s)
