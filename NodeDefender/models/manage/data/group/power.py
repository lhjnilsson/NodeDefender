from datetime import datetime, timedelta
from ....SQL import PowerModel, GroupModel

def Latest(icpe):
    return PowerModel.query.filter_by(node = None, icpe = icpe, sensor = None).first()

def Get(icpe, from_date = (datetime.now() - timedelta(days=7)), to_date =
        datetime.now()):
    return session.query(PowerModel).filter(node == None, icpe == icpe, sensor == None, date > from_date, date
                                            < to_date)

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
        db.session.add(data)
    else:
        node.power.append(PowerModel(power, date))
        db.session.add(node)
    
    db.session.commit()
