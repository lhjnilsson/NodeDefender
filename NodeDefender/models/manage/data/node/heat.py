from datetime import datetime, timedelta
from ....SQL import HeatModel, NodeModel, iCPEModel
from ..... import db
from sqlalchemy import func
from sqlalchemy.sql import label

def Latest(node):
    node = NodeModel.query.filter(NodeModel.name == node).first()
    if not node:
        return False

    heat_data = db.session.query(HeatModel, \
                                  label('low', func.min(HeatModel.low)),
                                  label('high', func.max(HeatModel.high)),
                                  label('total', func.sum(HeatModel.average)),
                                  label('date', HeatModel.date)).\
            join(iCPEModel).\
            filter(iCPEModel.macaddr == node.icpe.macaddr).\
            order_by(HeatModel.date.desc()).\
            group_by(HeatModel.date).first()

    if not heat_data:
        return False
    
    return {'node' : node.name, 'date' : str(heat_data.date), 'low' : power_data.low,\
            'high' : heat_data.high, 'total' : power_data.total}

def Get(node, from_date = (datetime.now() - timedelta(days=7)), to_date =
        datetime.now()):
    node = NodeModel.query.filter(NodeModel.name == node).first()
    if not node:
        return False
    
    heat_data = db.session.query(HeatModel, \
                                  label('low', func.min(HeatModel.low)),
                                  label('high', func.max(HeatModel.high)),
                                  label('total', func.sum(HeatModel.average)),
                                  label('date', HeatModel.date)).\
            join(iCPEModel).\
            filter(iCPEModel.macaddr == node.icpe.macaddr).\
            filter(HeatModel.date > from_date).\
            filter(HeatModel.date < to_date).\
            group_by(HeatModel.date).all()

    if not heat_data:
        return False
    ret_json = {'node' : node.name}
    ret_json['heat'] = []
    for data in heat_data:
        ret_json['heat'].append({'date' : str(data.date), 'low' : data.low, 'high' : data.high,
                                    'total' : data.total})
    return ret_json
