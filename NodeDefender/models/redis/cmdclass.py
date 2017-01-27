from . import redisconn
from ... import celery
from datetime import datetime
from .decorators import LookupCmdclass
'''
Common Format
    {
    cmdclass
    cmdname
    last_updated
    ... Dynamic per Cmdclass
    }

'''
@redisconn
@LookupCmdclass
def Load(cmdclass, conn):
    if cmdclass is None:
        return None
    conn.sadd(cmdclass.sensor.icpe.mac + cmdclass.sensor.sensorid +\
              ":classes", cmdclass.classname)
    return conn.hmset(cmdclass.sensor.icpe.mac + \
                      cmdclass.sensor.sensorid + \
                      cmdclass.classname, \
                        {
                            'cmdclass' : cmdclass.cmdclass,
                           'cmdname' : cmdclass.cmdname,
                           'last_updated' : datetime.now,
                           'loaded_at' : datetime.now,
                       })

@redisconn
def Get(mac, sensorid, cmdclass, conn):
    return conn.hgetall(mac + sensorid + cmdclass)

@redisconn
def Save(mac, sensorid, cmd, conn, **kwargs):
    cmdclass = conn.hgetall(mac + sensorid + cmd)
    for key, value in kwargs.items():
        cmdclass[key] = value

    return conn.hmset(mac + sensorid + cmd, cmdclass)
