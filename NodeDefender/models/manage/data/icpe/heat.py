from datetime import datetime, timedelta
from ....SQL import HeatModel

def Latest(icpe):
    return HeatModel.query.filter_by(node = None, icpe = icpe, sensor = None).first()

def Get(icpe, from_date = (datetime.now() - timedelta(days=7)), to_date =
        datetime.now()):
    return session.query(HeatModel).filter(node == None, icpe == icpe, sensor == None, date > from_date, date
                                            < to_date)

def Put(icpe, heat, date = datetime.now()):
    date = date.replace(minute=0, second=0, microsecond=0)
    data = session.query(HeatModel).filter(node == None, icpe == icpe, sensor == None, date == date)
    if data:
        heat = (data.heat / 2)
        data.precision += 1
    else:
        heat = HeatModel(icpe = icpe, heat = heat, date = date)
    db.session.add(heat)
    db.session.commit()
