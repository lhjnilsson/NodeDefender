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
    
    return {'node' : node.name, 'date' : power_data.date, 'low' : power_data.low,\
            'high' : power_data.high, 'total' : power_data.total}

def Get(node, from_date = (datetime.now() - timedelta(days=7)), to_date =
        datetime.now()):
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
            filter(PowerModel.date > from_date).\
            filter(PowerModel.date < to_date).\
            group_by(PowerModel.date).all()

    if not power_data:
        return False
    ret_json = {'node' : node.name}
    ret_json['power'] = []
    for data in power_data:
        ret_json['power'].append({data.date : {'low' : data.low, 'high' : data.high,
                                    'total' : data.total}})
    return ret_json
