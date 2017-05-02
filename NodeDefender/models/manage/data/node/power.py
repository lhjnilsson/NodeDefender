from datetime import datetime, timedelta
from ....SQL import PowerModel, NodeModel, iCPEModel, GroupModel, SensorModel
from ..... import db
from sqlalchemy import func
from sqlalchemy.sql import label
from itertools import groupby

def Current(node):
    node = db.session.query(NodeModel).filter(NodeModel.name ==
                                                node).first()
    if node is None:
        return False
    
    ret_data = []
    node_data = {}
    node_data['name'] = node.name
    node_data['power'] = 0.0
    for sensor in node.icpe.sensors:
        if not sensor.power:
            continue

        sensor_data = {}
        sensor_data['name'] = sensor.name
        sensor_data['sensorid'] = sensor.sensorid
        sensor_data['icpe'] = sensor.icpe.macaddr
        
        min_ago = (datetime.now() - timedelta(hours=0.5))
        latest_power =  db.session.query(PowerModel,\
                    label('sum', func.sum(PowerModel.average)),
                    label('count', func.count(PowerModel.average))).\
                    join(iCPEModel).\
                    join(SensorModel).\
                    filter(iCPEModel.macaddr == node.icpe.macaddr).\
                    filter(SensorModel.sensorid == sensor.sensorid).\
                    filter(PowerModel.date > min_ago).first()
        
        if latest_power.count:
            sensor_data['power'] = latest_power.sum / latest_power.count
            node_data['power'] += sensor_data['power']
        else:
            sensor_data['power'] = 0.0

        ret_data.append(sensor_data)

    ret_data.append(node_data)
    return ret_data

def Average(node):
    node = db.session.query(NodeModel).filter(NodeModel.name ==
                                               node).first()
    if node is None:
        return False

    min_ago = (datetime.now() - timedelta(hours=0.5))
    day_ago = (datetime.now() - timedelta(days=1))
    week_ago = (datetime.now() - timedelta(days=7))
    month_ago = (datetime.now() - timedelta(days=30))
    ret_data = []
    node_data = {}
    node_data['name'] = node.name
    node_data['current'] = 0.0
    node_data['daily'] = 0.0
    node_data['weekly'] = 0.0
    node_data['monthly'] = 0.0 

    current_power = db.session.query(PowerModel,\
                label('sum', func.sum(PowerModel.average)),
                label('count', func.count(PowerModel.average))).\
                join(iCPEModel).\
                filter(iCPEModel.macaddr == node.icpe.macaddr).\
                filter(PowerModel.date > min_ago).first()
    
    daily_power = db.session.query(PowerModel,\
                label('sum', func.sum(PowerModel.average)),
                label('count', func.count(PowerModel.average))).\
                join(iCPEModel).\
                filter(iCPEModel.macaddr == node.icpe.macaddr).\
                filter(PowerModel.date > day_ago).first()
    
    weekly_power = db.session.query(PowerModel,\
                label('sum', func.sum(PowerModel.average)),
                label('count', func.count(PowerModel.average))).\
                join(iCPEModel).\
                filter(iCPEModel.macaddr == node.icpe.macaddr).\
                filter(PowerModel.date > week_ago).first()

    monthly_power = db.session.query(PowerModel,\
                label('sum', func.sum(PowerModel.average)),
                label('count', func.count(PowerModel.average))).\
                join(iCPEModel).\
                filter(iCPEModel.macaddr == node.icpe.macaddr).\
                filter(PowerModel.date > month_ago).first()
    
    if current_power.count:
        current_power = (current_power.sum / current_power.count)
    else:
        current_power = 0.0

    if daily_power.count:
        daily_power = (daily_power.sum / daily_power.count)
    else:
        daily_power = 0.0

    if weekly_power.count:
        weekly_power = (weekly_power.sum / weekly_power.count)
    else:
        weekly_power = 0.0

    if monthly_power.count:
        monthly_power = (monthly_power.sum / monthly_power.count)
    else:
        monthly_power = 0.0

    node_data['current'] = current_power

    node_data['daily'] = daily_power

    node_data['weekly'] = weekly_power

    node_data['monthly'] = monthly_power

    return node_data

def Chart(node):    
    from_date = (datetime.now() - timedelta(days=30))
    to_date = datetime.now()
    
    node = db.session.query(NodeModel).filter(NodeModel.name ==
                                                node).first()
    if node is None:
        return False

    ret_data = []
    
    for sensor in node.icpe.sensors:
        if not sensor.power:
            continue
        
        power_data = db.session.query(PowerModel).\
                join(iCPEModel).\
                join(SensorModel).\
                filter(iCPEModel.macaddr == node.icpe.macaddr).\
                filter(SensorModel.sensorid == sensor.sensorid).\
                filter(PowerModel.date > from_date).\
                filter(PowerModel.date < to_date).all()

        if not power_data:
            continue
        
        sensor_data = {}
        sensor_data['name'] = sensor.name
        sensor_data['sensorid'] = sensor.sensorid
        sensor_data['icpe'] = sensor.icpe.macaddr

        sensor_data['power'] = []
        grouped_data = [list(v) for k, v in groupby(power_data, lambda p:
                                                    p.date)]

        for data in grouped_data:
            entry = {'date' : str(data[0].date)}
            for power in data:
                try:
                    entry['value'] = (power.average + entry['power']) / 2
                except KeyError:
                    entry['value'] = power.average
            sensor_data['power'].append(entry)

        ret_data.append(sensor_data)
    
    return ret_data
