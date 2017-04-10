from datetime import datetime, timedelta
from ....SQL import PowerModel, GroupModel

def Latest(group):
    return PowerModel.query.join(GroupModel).\
            filter(GroupModel.name == group).first()

def Get(group, from_date = (datetime.now() - timedelta(days=7)), to_date =
        datetime.now()):
    return PowerModel.query.join(GroupModel).\
            filter(PowerModel.date > from_date).\
            filter(PowerModel.date < to_date).\
            filter(GroupModel.name == group).all()

def Put(group, power, date = datetime.now()):
    date = date.replace(minute=0, second=0, microsecond=0)
    data, group = PowerModel.query.join(GroupModel).\
            filter(PowerModel.date == date).\
            filter(GroupModel.name == node).first()

    if data:
        if power > data.power:
            data.high = power

        if power < data.power:
            data.low = power

        data.average = (data.average + power) / 2
        data.total = data.total + power
        db.session.add(data)
    else:
        node.power.append(PowerModel(power, date))
        db.session.add(node)
    
    db.session.commit()
    return True
