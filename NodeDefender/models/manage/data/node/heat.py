from datetime import datetime, timedelta
from ....SQL import HeatModel, NodeModel, iCPEModel, GroupModel, SensorModel
from ..... import db
from sqlalchemy import func
from sqlalchemy.sql import label
from itertools import groupby

def Current(node):
    node = db.session.query(NodeModel).filter(NodeModel.name ==
                                                node).first()
    if node is None or not node.icpe or not node.icpe.sensors:
        return False
    
    ret_data = []
    node_data = {}
    node_data['name'] = node.name
    node_data['heat'] = 0.0
    for sensor in node.icpe.sensors:
        if not sensor.heat:
            continue

        sensor_data = {}
        sensor_data['name'] = sensor.name
        sensor_data['sensorid'] = sensor.sensorid
        sensor_data['icpe'] = sensor.icpe.macaddr
        
        min_ago = (datetime.now() - timedelta(hours=0.5))
        latest_heat =  db.session.query(HeatModel,\
                    label('sum', func.sum(HeatModel.average)),
                    label('count', func.count(HeatModel.average))).\
                    join(HeatModel.icpe).\
                    join(HeatModel.sensor).\
                    filter(iCPEModel.macaddr == node.icpe.macaddr).\
                    filter(SensorModel.sensorid == sensor.sensorid).\
                    filter(HeatModel.date > min_ago).first()
        
        if latest_heat.count:
            sensor_data['heat'] = latest_heat.sum / latest_heat.count
            node_data['heat'] += sensor_data['heat']
        else:
            sensor_data['heat'] = 0.0

        ret_data.append(sensor_data)

    ret_data.append(node_data)
    return node_data

def Average(node):
    node = db.session.query(NodeModel).filter(NodeModel.name ==
                                               node).first()
    if node is None or not node.icpe or not node.icpe.sensors:
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

    current_heat = db.session.query(HeatModel,\
                label('sum', func.sum(HeatModel.average)),
                label('count', func.count(HeatModel.average))).\
                join(HeatModel.icpe).\
                filter(iCPEModel.macaddr == node.icpe.macaddr).\
                filter(HeatModel.date > min_ago).first()
    
    daily_heat = db.session.query(HeatModel,\
                label('sum', func.sum(HeatModel.average)),
                label('count', func.count(HeatModel.average))).\
                join(HeatModel.icpe).\
                filter(iCPEModel.macaddr == node.icpe.macaddr).\
                filter(HeatModel.date > day_ago).first()
    
    weekly_heat = db.session.query(HeatModel,\
                label('sum', func.sum(HeatModel.average)),
                label('count', func.count(HeatModel.average))).\
                join(HeatModel.icpe).\
                filter(iCPEModel.macaddr == node.icpe.macaddr).\
                filter(HeatModel.date > week_ago).first()

    monthly_heat = db.session.query(HeatModel,\
                label('sum', func.sum(HeatModel.average)),
                label('count', func.count(HeatModel.average))).\
                join(HeatModel.icpe).\
                filter(iCPEModel.macaddr == node.icpe.macaddr).\
                filter(HeatModel.date > month_ago).first()
    
    if current_heat.count:
        current_heat = (current_heat.sum / current_heat.count)
    else:
        current_heat = 0.0

    if daily_heat.count:
        daily_heat = (daily_heat.sum / daily_heat.count)
    else:
        daily_heat = 0.0

    if weekly_heat.count:
        weekly_heat = (weekly_heat.sum / weekly_heat.count)
    else:
        weekly_heat = 0.0

    if monthly_heat.count:
        monthly_heat = (monthly_heat.sum / monthly_heat.count)
    else:
        monthly_heat = 0.0

    node_data['current'] = current_heat

    node_data['daily'] = daily_heat

    node_data['weekly'] = weekly_heat

    node_data['monthly'] = monthly_heat

    return node_data

def Chart(node):    
    from_date = (datetime.now() - timedelta(days=30))
    to_date = datetime.now()
    
    node = db.session.query(NodeModel).filter(NodeModel.name ==
                                                node).first()
    if node is None or not node.icpe or not node.icpe.sensors:
        return False

    ret_data = []
    
    for sensor in node.icpe.sensors:
        if not sensor.heat:
            continue
        
        heat_data = db.session.query(HeatModel).\
                join(HeatModel.icpe).\
                join(HeatModel.sensor).\
                filter(iCPEModel.macaddr == node.icpe.macaddr).\
                filter(SensorModel.sensorid == sensor.sensorid).\
                filter(HeatModel.date > from_date).\
                filter(HeatModel.date < to_date).all()

        if not heat_data:
            continue
        
        sensor_data = {}
        sensor_data['name'] = sensor.name
        sensor_data['sensorid'] = sensor.sensorid
        sensor_data['icpe'] = sensor.icpe.macaddr

        sensor_data['heat'] = []
        grouped_data = [list(v) for k, v in groupby(heat_data, lambda p:
                                                    p.date)]

        for data in grouped_data:
            entry = {'date' : str(data[0].date)}
            for heat in data:
                try:
                    entry['value'] = (heat.average + entry['heat']) / 2
                except KeyError:
                    entry['value'] = heat.average
            sensor_data['heat'].append(entry)

        ret_data.append(sensor_data)
    
    return ret_data
