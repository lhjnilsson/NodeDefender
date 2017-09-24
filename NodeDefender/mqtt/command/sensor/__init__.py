import NodeDefender.mqtt.command.sensor.info

def sensor_info(mac_address, sensor_id):
    NodeDefender.mqtt.command.sensor.info.qry(mac_address, sensor_id)
    return True
