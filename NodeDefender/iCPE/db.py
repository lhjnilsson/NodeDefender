'''
Common Redis Format

    For iCPE:
        {
        MAC
        IP Address
        Online
        Battery
        Loaded At
        Last Online
        }

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

def Load(icpe, sensor = None):
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


def LoadCmdclass(sensor, data = {}):

def Save(data, icpe, nodeid = None):
    pass 

def Get(mac, sensorid = None):
    return conn.hgetall(mac + sensorid)
