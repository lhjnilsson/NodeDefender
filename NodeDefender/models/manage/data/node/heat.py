from datetime import datetime, timedelta
from ....SQL import HeatModel

def Latest(node):
    return HeatModel.query.filter_by(name = node).first()

def Get(node, from_date = (datetime.now() - timedelta(days=7)), to_date =
        datetime.now()):
    return session.query(HeatModel).filter(name == node, date > from_date, date
                                            < to_date)

def Put(node, heat, date):
    data = session.query(HeatModel).filter(name == node, date == date)
    if data:
        heat = (data.heat / 2)
        data.presision += 1
    else:
        heat = HeatModel(heat, date)
    db.session.add(heat)
    db.session.commit()
