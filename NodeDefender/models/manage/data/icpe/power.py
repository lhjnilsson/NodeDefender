from datetime import datetime, timedelta
from ...SQL import PowerModel

def Latest(icpe):
    return PowerModel.query.filter_by(node = None, icpe = icpe, sensor = None).first()

def Get(icpe, from_date = (datetime.now() - timedelta(days=7)), to_date =
        datetime.now()):
    return session.query(PowerModel).filter(node == None, icpe == icpe, sensor == None, date > from_date, date
                                            < to_date)

def Put(icpe, power, date = datetime.now()):
    date = date.replace(minute=0, second=0, microsecond=0)
    data = session.query(PowerModel).filter(node == None, icpe == icpe, sensor == None, date == date)
    if data:
        power = (data.power / 2)
        data.precision += 1
    else:
        power = PowerModel(icpe = icpe, power = power, date = date)
    db.session.add(power)
    db.session.commit()
