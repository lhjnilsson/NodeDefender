from datetime import datetime, timedelta
from ....SQL import PowerModel, GroupModel, iCPEModel
from ..... import db
from sqlalchemy import func
from sqlalchemy.sql import label
from itertools import groupby

def Latest(group):
    group = GroupModel.query.filter(GroupModel.name == group).first()
    if not group:
        return False

    #icpes = [[icpe.macaddr for icpe in node.icpes] for node in group.nodes]
    icpes = [node.icpe.macaddr for node in group.nodes]

    power_data = db.session.query(PowerModel, \
                                  label('low', func.min(PowerModel.low)),
                                  label('high', func.max(PowerModel.high)),
                                  label('total', func.sum(PowerModel.average)),
                                  label('date', PowerModel.date)).\
            join(iCPEModel).\
            filter(iCPEModel.macaddr.in_(*[icpes])).\
            order_by(PowerModel.date.desc()).\
            group_by(PowerModel.date).first()

    if not power_data:
        return False
    
    return {'group' : group.name, 'date' : str(power_data.date), 'low' : power_data.low,\
            'high' : power_data.high, 'total' : power_data.total}

def Get(group, from_date = None, to_date = None):
    if from_date is None:
        from_date = (datetime.now() - timedelta(days=7))
    if to_date is None:
        to_date = datetime.now()
    
    group = GroupModel.query.filter(GroupModel.name == group).first()
    if not group:
        return False
    
    #icpes = [[icpe.macaddr for icpe in node.icpes] for node in group.nodes]
    icpes = [node.icpe.macaddr for node in group.nodes]
    
    power_data = db.session.query(PowerModel).\
            join(iCPEModel).\
            filter(iCPEModel.macaddr.in_(*[icpes])).\
            filter(PowerModel.date > from_date).\
            filter(PowerModel.date < to_date).all()

    if not power_data:
        return False

    grouped_data = [list(v) for k, v in groupby(power_data, lambda p: p.date)]
    
    ret_json = {'group' : group.name}
    ret_json['power'] = []
    for group in grouped_data:
        data = {'date' : str(group[0].date)}
        for entry in group:
            data[entry.sensor.sensorid] = entry.average
        ret_json['power'].append(data)
    
    return ret_json
