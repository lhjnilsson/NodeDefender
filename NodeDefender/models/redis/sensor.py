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
        commandclass = {
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
@LookupSensor
@redisconn
def Load(sensor, conn):
    if sensor is None:
        return None
    s = {
        'name' : sensor.name,
        'sensorid' : sensor.sensorid,
        'librarytype' : sensor.librarytype,
        'devicetype' : sensor.devicetype,
        'productid' : sensor.productid,
        'manufacturerid' : sensor.manufacturerid,
        'brand' : sensor.brand
    }
    logger.info("Loaded Sensor {}:{} from Object".format(sensor.icpe.macaddr,
                                                         sensor.sensorid))
    conn.sadd(sensor.icpe.macaddr + sensor.sensorid + ':commandclasses', \
              [commandclass.name for commandclass in sensor.commandclasses])
    return conn.hmset(sensor.icpe.macaddr + sensor.sensorid, s)

@redisconn
def Get(mac, sensorid, conn):
    return conn.hgetall(mac + sensorid)

@redisconn
def Save(mac, sid, conn, **kwargs):
    logger.info("Save data for sensor {}:{}. Data: {}".\
                format(mac, sid, kwargs))
    return conn.hmset(mac + str(sid), kwargs)

@redisconn
def Fields(mac, sensorid, conn):
    return conn.smembers(mac + sensorid + ':fields')

@redisconn
def Commandclasses(mac, sensorid, conn):
    return conn.smembers(mac + sensorid + ':commandclasses')
