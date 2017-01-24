from ...models.manage import sensor as SensorSQL
from . import redisconn
from .. import mqtt, zwave
from ... import celery
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
        'sensorid' : str(sensor.sensorid),
        'roletype' : sensor.roletype,
        'devicetype' : sensor.devicetype,
        'unsupported' : unsupported,
        'cmdclass' : supported
    }
    if not len(supported):
        mqtt.sensor.Query(sensor.icpe.mac, str(sensor.sensorid))

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
def Save(mac, sid, conn, **kwargs):
    return conn.hmset(mac + str(sid), kwargs)

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
    
    for classnum in classes:
        classname, types = zwave.Info(classnum)
        
        if classname is None:
            pass

        if types:
            mqtt.sensor.Sup(mac, sensorid, classname, **mqttsrc)

        SensorSQL.AddClass(mac, sensorid, classnum, classname)
    
    return Load(mac, sensorid)

def AddClassTypes(mac, sensorid, cmdclass, classtypes):
    if SensorSQL.Get(mac, sensorid) is None:
        raise LookupError('Sensor not found')

    SensorSQL.AddClassTypes(mac, sensorid, classname, classtypes)
    return Load(mac, sensorid)
