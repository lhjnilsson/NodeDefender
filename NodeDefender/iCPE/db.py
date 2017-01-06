from .decorators import SensorRules
import redis


pool = redis.ConnectionPool(host='localhost', port=6379, db=0)

def LoadSensor(icpe, sensor):
    if sensor:
        s = {'id' : sensor.sensor_id,
             'classes' : [],
             'unsupported' : [cls for cls in sensor.classes.class_id],
             'name' : sensor.name,
             'roletype' : sensor.roletype,
             'devicetype' : sensor.devicetype,
             'data' :  []}
        conn.hmset(icpe.mac + str(sensor.sensor_id), s)
        return
        
    # If No Sensor, Load the whole iCPE and all registered sensors
    d = {'mac' : icpe.mac, 'ipaddr' : icpe.ipaddr, 'online' : False, 'loaded' :
         datetime.now(), 'lastonline' : None}
    conn.hmset(icpe.mac, d)
    
    for sensor in icpe.sensors:
        s = {'id': sensor.sensor_id,
             'classes' : {},
             'unsupported' : [cls for cls in sensor.classes.class_id],
             'name' : sensor.name,
             'roletype' : sensor.roletype,
             'devicetype' : sensor.devicetype,
             'data' :  []}
        conn.hmset(icpe.mac + str(sensor.sensor_id), s)
    return

@SensorRules
def UpdateSensor(topic, sensor, evt):
    sensor[evt.cmdclass] = evt
    Save(sensor, topic.mac, topic.sensorid)
    return True

def LoadCmdclass(sensor, data = {}):
    pass

def Save(data, icpe, sensorid = None):
    pass 

def Get(mac, sensorid = ""):
    conn = redis.Redis(connection_pool=pool)
    data = conn.hgetall(mac + sensorid)
    if len(data):
        return data
    else:
        return None
