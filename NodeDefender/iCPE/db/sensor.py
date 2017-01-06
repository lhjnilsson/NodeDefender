from ....models.manage import sensor as SensorSQL

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
def Create(mac, sensorid):
    if SensorSQL.Get(mac, sensorid):
        raise ValueError('Already exists')
    return SensorSQL.Create(mac, sensorid)

def Load(mac, sensorid):
    sensor = SensorSQL.load(mac, sensorid)
    if sensor is None:
        return None
    
    conn = StrictRedis(connection_pool=pool)
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

def Save(mac, sensorid, **kwargs):
    conn = StrictRedis(connection_pool=pool)
    s = conn.hmgetall(mac + sensorid)
    for key, value in kwargs:
        s[key] = value

    conn.hmset(mac + sensorid, s)
