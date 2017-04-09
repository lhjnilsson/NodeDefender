from datetime import datetime, timedelta
from ....SQL import PowerModel, iCPEModel

def Latest(icpe):
    return PowerModel.query.filter_by(node = None, icpe = icpe, sensor = None).first()

def Get(icpe, from_date = (datetime.now() - timedelta(days=7)), to_date =
        datetime.now()):
    return session.query(PowerModel).filter(node == None, icpe == icpe, sensor == None, date > from_date, date
                                            < to_date)

def Put(icpe, power, date = datetime.now()):
    date = date.replace(minute=0, second=0, microsecond=0)
    data, icpe = PowerModel.query.join(iCPEModel).\
            filter(PowerModel.date == date).\
            filter(iCPEModel.macaddr == icpe).first()

    if data:
        if power > data.power:
            data.high = power

        if power < data.power:
            data.low = power

        data.average = (data.average + power) / 2
        db.session.add(data)
    else:
        icpe.power.append(PowerModel(power, date))
        db.session.add(icpe) 
    
    db.session.commit()
    for node in icpe.nodes:
        NodeData.power.put(node.name, power, date)
