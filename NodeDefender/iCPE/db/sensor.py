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
def Load(mac, sensorid, conn):
    sensor = SensorSQL.Get(mac, sensorid)
    if sensor is None:
        return None
    try:
        supported, unsupported = zwave.Load(*[cmdclass for cmdclass in sensor.cmdclasses])
    except TypeError:
        supported = []
        unsupported = []

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
def LoadFromObject(sensor, conn):
    try:
        supported, unsupported = zwave.Load(*[cmdclass for cmdclass in sensor.cmdclasses])
    except TypeError:
        supported = []
        unsupported = []

    s = {
        'name' : sensor.name,
        'sensorid' : sensor.sensorid,
        'roletype' : sensor.roletype,
        'devicetype' : sensor.devicetype,
        'unsupported' : unsupported,
        'cmdclass' : supported
    }

    conn.hmset(sensor.icpe.mac + str(sensor.sensorid), s)
    return s

@redisconn
def Get(mac, sensorid, conn):
    sensor = conn.hgetall(mac + sensorid)
    if len(sensor):
        return sensor
    else:
        return None

@redisconn
def Save(mac, sensorid, conn, **kwargs):
    return conn.hmset(mac + sensorid, kwargs)

def CreateLoadQuery(mqttsrc, mac, sensorid):
    if Load(mac, sensorid) is not None:
        raise ValueError('Already exists')
    
    Create(mac, sensorid)
    Load(mac, sensorid)
    mqtt.sensor.Query(mac, sensorid, **mqttsrc)
    return True

def AddClass(mac, sensorid, *classes):
    if SensorSQL.Get(mac, sensorid) is None:
        raise LookupError('Sensor not found')
    
    for cls in classes:
        classname = zwave.Classname(cls)
        if classname is None:
            pass

        SensorSQL.AddClass(mac, sensorid, cls, classname)
    
    return True

def AddClassTypes(mac, sensorid, cmdclass, classtypes):
    if SensorSQL.Get(mac, sensorid) is None:
        raise LookupError('Sensor not found')

    SensorSQL.AddClassTypes(mac, sensorid, classname, classtypes)
