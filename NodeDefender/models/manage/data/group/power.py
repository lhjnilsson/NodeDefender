from datetime import datetime, timedelta
from ....SQL import PowerModel, GroupModel, iCPEModel
from ..... import db
from sqlalchemy import func
from sqlalchemy.sql import label
from itertools import groupby

def Current(*groups):
    groups = GroupModel.query.filter(GroupModel.name.in_(*[groups])).all()
    if groups is None:
        return False
    
    ret_data = []
    for group in groups:
        group_data = {}
        group_data['name'] = group.name
        icpes = [node.icpe.macaddr for node in group.nodes]
        min_ago = (datetime.now() - timedelta(mins=30))
        latest_power =  db.session.query(PowerModel,\
                    label('sum', func.sum(PowerModel.average)),
                    label('count', func.count(PowerModel.average))).\
                    join(iCPEModel).\
                    filter(iCPEModel.macaddr.in_(*[icpes])).\
                    filter(PowerModel.date > min_ago).first()
        group_data['power'] = latest_power.sum / latest_power.count
        ret_data.append(group_data)

    if len(ret_data) == 1:
        return ret_data[0]
    return ret_data

def Average(*groups):
    groups = GroupModel.query.filter(GroupModel.name.in_(*[groups])).all()
    if groups is None:
        return False
    
    day_ago = (datetime.now() - timedelta(days=1))
    week_ago = (datetime.now() - timdelta(days=7))
    month_ago = (datetime.now() - timedelta(months=1))
    ret_data = []
    for group in groups:
        group_data = {}
        group_data['name'] = group.name
        icpes = [node.icpe.macaddr for node in group.nodes]
        daily_power = db.session.query(PowerModel,\
                    label('sum', func.sum(PowerModel.average)),
                    label('count', func.count(PowerModel.average))).\
                    join(iCPEModel).\
                    filter(iCPEModel.macaddr.in_(*[icpes])).\
                    filter(PowerModel.date > day_ago).first()
        
        weekly_power = db.session.query(PowerModel,\
                    label('sum', func.sum(PowerModel.average)),
                    label('count', func.count(PowerModel.average))).\
                    join(iCPEModel).\
                    filter(iCPEModel.macaddr.in_(*[icpes])).\
                    filter(PowerModel.date > week_ago).first()

        monthly_power = db.session.query(PowerModel,\
                    label('sum', func.sum(PowerModel.average)),
                    label('count', func.count(PowerModel.average))).\
                    join(iCPEModel).\
                    filter(iCPEModel.macaddr.in_(*[icpes])).\
                    filter(PowerModel.date > month_ago).first()
        
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

        group_data['daily'] = daily_power
        group_data['weekly'] = weeky_power
        group_data['monthly'] = monthly_power
        ret_data.append(group_data)

    if len(ret_data) == 1:
        return ret_data[0]
    return ret_data

def Chart(*groups):
    groups = GroupModel.query.filter(GroupModel.name.in_(*[groups])).all()
    if groups is None:
        return False
    ret_data = []
    
    for group in groups:
        icpes = [node.icpe.macaddr for node in group.nodes]
        
        power_data = db.session.query(PowerModel).\
                join(iCPEModel).\
                filter(iCPEModel.macaddr.in_(*[icpes])).\
                filter(PowerModel.date > from_date).\
                filter(PowerModel.date < to_date).all()

        if not power_data:
            return False

        grouped_data = [list(v) for k, v in groupby(power_data, lambda p: p.icpe)]

        ret_list = []
        for data in grouped_data:
            entry = {'node' : data[0].icpe.node.name}
            entry['data'] = []
            for power in data:
                entry['data'].append({'date' : str(power.date), 'power' :
                                     power.average})
            ret_list.append(entry)

        ret_data.append(ret_list)

    if len(ret_data) == 1:
        return ret_data[0]
    return ret_data

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

def Nodes(group, from_date = None, to_date = None):
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

    grouped_data = [list(v) for k, v in groupby(power_data, lambda p: p.icpe)]

    ret_list = []
    for data in grouped_data:
        entry = {'node' : data[0].icpe.node.name}
        entry['data'] = []
        for power in data:
            entry['data'].append({'date' : str(power.date), 'power' :
                                 power.average})
        ret_list.append(entry)

    return ret_list


    for group in grouped_data:
        data = {'date' : str(group[0].date)}
        for entry in group:
            name = entry.icpe.node.name
            try:
                data[name] = (data[name] + entry.average) / 2
            except KeyError:
                data[name] = entry.average

            ret_json['nodes'].add(name)
        ret_json['power'].append(data)
    ret_json['nodes'] = list(ret_json['nodes'])
    return ret_json
