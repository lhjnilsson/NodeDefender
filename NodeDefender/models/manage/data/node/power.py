from datetime import datetime, timedelta
from ....SQL import PowerModel, NodeModel

def Latest(node):
    return PowerModel.query.join(NodeModel).\
            filter(NodeModel.name == node).first()

def Get(node, from_date = (datetime.now() - timedelta(days=7)), to_date =
        datetime.now()):
    return PowerModel.query.join(NodeModel).\
            filter(PowerModel.date > from_date).\
            filter(PowerModel.date < to_date).\
            filter(NodeModel.name == node).all()

def Put(node, power, date = datetime.now()):
    date = date.replace(minute=0, second=0, microsecond=0)
    data, node = PowerModel.query.join(NodeModel).\
            filter(PowerModel.date == date).\
            filter(NodeModel.name == node).first()

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
    for group in node.groups:
        GroupData.power.put(group.name, power, date)
