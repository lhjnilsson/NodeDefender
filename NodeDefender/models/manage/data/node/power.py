from datetime import datetime, timedelta
from ....SQL import PowerModel, NodeModel, iCPEModel
from ..... import db
from sqlalchemy import func
from sqlalchemy.sql import label

def Latest(node):
    node = NodeModel.query.filter(NodeModel.name == node).first()
    if not node:
        return False

    power_data = db.session.query(PowerModel, \
                                  label('low', func.min(PowerModel.low)),
                                  label('high', func.max(PowerModel.high)),
                                  label('total', func.sum(PowerModel.average)),
                                  label('date', PowerModel.date)).\
            join(iCPEModel).\
            filter(iCPEModel.macaddr == node.icpe.macaddr).\
            order_by(PowerModel.date.desc()).\
            group_by(PowerModel.date).first()

    if not power_data:
        return False
    
    return {'node' : node.name, 'date' : str(power_data.date), 'low' : power_data.low,\
            'high' : power_data.high, 'total' : power_data.total}

def Get(node, from_date = (datetime.now() - timedelta(days=7)), to_date =
        datetime.now()):
    node = NodeModel.query.filter(NodeModel.name == node).first()
    if not node:
        return False
    
    power_data = db.session.query(PowerModel).\
            join(iCPEModel).\
            filter(iCPEModel == node.icpe).\
            filter(PowerModel.date > from_date).\
            filter(PowerModel.date < to_date).all()

    if not power_data:
        return False

    grouped_data = [list(v) for k, v in groupby(power_data, lambda p: p.date)]
    
    ret_json = {'node' : node.name}
    ret_json['power'] = []
    for group in grouped_data:
        data = {'date' : str(group[0].date)}
        for entry in group:
            data[entry.sensor.sensorid] = entry.average
        ret_json['power'].append(data)
    
    return ret_json
