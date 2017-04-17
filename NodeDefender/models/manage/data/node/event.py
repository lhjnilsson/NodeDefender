from datetime import datetime, timedelta
from ....SQL import EventModel

def Latest(node):
    return EventModel.query.filter_by(name = node).first()

def Get(node, from_date = (datetime.now() - timedelta(days=7)), to_date =
        datetime.now()):
    return session.query(EventModel).filter(name == node, date > from_date, date
                                            < to_date)

def Put(node, power, date):
    data = session.query(EventModel).filter(name == node, date == date)
    if data:
        power = (data.power / 2)
        data.presision += 1
    else:
        power = EventModel(power, date)
    db.session.add(power)
    db.session.commit()
