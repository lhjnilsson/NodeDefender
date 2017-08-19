from NodeDefender.icpe.zwave import commandclass, devices

def event(mac, sensoid, classname, **payload):
    return True
    try:
        return eval('commandclass' + '.' + classname + '.event')\
                (mac, sensorid, classname, **payload)
    except NameError:
        pass
