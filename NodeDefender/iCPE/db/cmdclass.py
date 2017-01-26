def AddClass(mac, sensorid, *classes):
    if SensorSQL.Get(mac, sensorid) is None:
        raise LookupError('Sensor not found')
    for classnum in classes:
        try:
            classname, types = zwave.Info(classnum)
        except TypeError:
            print("Error adding class ", classnum)
            return

        if classname is None:
            pass

        if types:
            mqtt.sensor.Sup(mac, sensorid, classname)

        SensorSQL.AddClass(mac, sensorid, classnum, classname)
    
    return Load(mac, sensorid)

def AddClassTypes(mac, sensorid, cmdclass, classtypes):
    if SensorSQL.Get(mac, sensorid) is None:
        raise LookupError('Sensor not found')

    SensorSQL.AddClassTypes(mac, sensorid, classname, classtypes)
    return Load(mac, sensorid)
