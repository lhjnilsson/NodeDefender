

def sensor_info(icpe, sensorid, payload):
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
    
    save_sql(sensor)
    NodeDefender.db.redis.sensor.load(sensor)
    NodeDefender.db.redis.sensor.update(sensor)
