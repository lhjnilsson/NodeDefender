from ...models.manage import sensor as SensorSQL
from . import redisconn
from .. import mqtt

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
def Create(mqtt, mac, sensorid, conn):
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

def CreateLoadQuery(mqtt, mac, sensorid):
    if Load(mac, sensorid) is not None:
        raise ValueError('Already exists')
    
    Create(mac, sensorid)
    Load(mac, sendorid)
    mqtt.sensor.Query(mac, sensorid, conn)
    return True


@redisconn
def Load(mac, sensorid, conn):
    sensor = SensorSQL.Get(mac, sensorid)
    if sensor is None:
        return None
    
    s = {
        'alias' : sensor.alias,
        'sensorid' : sensor.sensorid,
        'roletype' : sensor.roletype,
        'devicetype' : sensor.devicetype,
        'unsupported' : [cmdclass for cmdclass in sensor.unsupported],
        'cmdclass' : {cmdclass : zwave.Load(cmdclass, classtypes)\
                      for cmdclass in sensor.cmdclasses}
    }

    conn.hmset(icpe.mac + sensor_id, s)
    return s

@redisconn
def Save(mac, sensorid, conn, **kwargs):
    s = conn.hgetall(mac + sensorid)
    for key, value in kwargs:
        s[key] = value

    conn.hmset(mac + sensorid, s)
