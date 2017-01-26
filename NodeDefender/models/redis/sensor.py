from ...models.manage import sensor as SensorSQL
from . import redisconn
from ... import celery
from datetime import datetime
from . import logger
from .decorators import LookupSensor
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
@LookupSensor
def Load(sensor, conn):
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
    logger.info("Loaded Sensor {}:{} from Object".format(mac, sensorid))
    conn.sadd(sensor.icpe.mac + sensor.sensorid, \
              [cmdclass.cmdname for cmdclass in sensor.cmdclasses])
    return conn.hmset(sensor.icpe.mac + sensor.sensorid, s)

@redisconn
def Get(mac, sensorid, conn):
    sensor = conn.hgetall(mac + sensorid)
    if len(sensor):
        return sensor
    else:
        return None

@redisconn
def Save(mac, sid, conn, **kwargs):
    logger.info("Save data for sensor {}:{}. Data: {}".\
                format(mac, sid, kwargs))
    return conn.hmset(mac + str(sid), kwargs)

@redisconn
def Cmdclasses(mac, sensorid, conn):
    return conn.smembers(mac + sensorid)
