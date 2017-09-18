import NodeDefender

def sensor_info(icpe, sensorid, **payload):
    sensor = NodeDefender.db.sensor.get_sql(icpe, sensor)
    
    sensor.sleepable = bool(eval(payload['sleepable']))
    sensor.wakeup_interval = payload['wakeup_interval']

    info = NodeDefender.icpe.zwave.devices.info(vendorid, productid)
    if info is None:
        return False
    try:
        sensor.vendor_id = vendorid
        sensor.product_id = productid
        sensor.product_type = info['ProductTypeId']
        sensor.vendor_name = info['Brand']
        sensor.product_name = info['Name']
        sensor.device_type = info['DeviceType']
        sensor.library_type = info['LibraryType']
    except KeyError:
        print(info)
        return False

    commandclasses = sensor.commandclasses()
    for commandclass in payload['clslist_N']:
        if commandclass not in commandclasses:
            NodeDefender.db.commandclass.create(icpe, sensorid, commandclass)

    for commandclass in commandclasses:
        if commandclass not in payload['clslist_N']:
            NodeDefender.db.commandclass.delete(icpe, sensorid, commandclass)

    NodeDefender.db.sensor.save_sql(sensor)
    NodeDefender.db.redis.sensor.load(sensor)
    return NodeDefender.db.redis.sensor.update(sensor)

def commandclass_types(icpe, sensorid, commandclass_name, **payload):
    classtypes = payload['typelist'].split(',')
    for classtype in classtypes:
        if not NodeDefender.db.commandclass.\
           get_type(icpe, sensorid, commandclass_name, classtype):
            NodeDefender.db.commandclass.\
                    add_type(icpe, sensorid, commandclass_name, classtype)
    return True
