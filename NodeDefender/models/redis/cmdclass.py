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
@LookupCmdclass
@redisconn
def Load(cmdclass, conn):
    if not cmdclass:
        return None
    if not cmdclass.supported:
        return False

    conn.sadd(cmdclass.sensor.icpe.macaddr + cmdclass.sensor.sensorid +\
              ":classes", cmdclass.classname)
    return conn.hmset(cmdclass.sensor.icpe.macaddr + \
                      cmdclass.sensor.sensorid + \
                      cmdclass.classname, \
                        {
                            'cmdclass' : cmdclass.classnumber,
                           'cmdname' : cmdclass.classname,
                           'last_updated' : str(datetime.now()),
                           'loaded_at' : str(datetime.now()),
                       })

@redisconn
def Get(mac, sensorid, cmdclass, conn):
    return conn.hgetall(mac + sensorid + cmdclass)

@redisconn
def Fields(mac, sensorid, cmdclass, conn):
    fieldlist = conn.smembers(mac + sensorid + cmdclass + ':fields')
    return [field for field in fieldlist]

@redisconn
def Save(mac, sensorid, cmd, conn, **kwargs):
    for key, value in kwargs.items():
        conn.hmset(mac + sensorid + cmd, {key : value})
        
    conn.hmset(mac + sensorid + cmd, {'last_updated' : str(datetime.now())})
    return True
