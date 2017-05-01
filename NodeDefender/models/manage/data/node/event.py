from datetime import datetime, timedelta
from ....SQL import EventModel, NodeModel
from ..... import db
from sqlalchemy import or_


def Latest(node):
    return EventModel.query.filter_by(name = node).first()

def Get(node, from_date = (datetime.now() - timedelta(days=7)), to_date =
        datetime.now()):
    return db.session.query(EventModel).join(NodeModel).\
            filter(NodeModel.name == node, EventModel.date > from_date,\
                   EventModel.date < to_date).all()

def Put(node, power, date):
    data = session.query(EventModel).filter(name == node, date == date)
    if data:
        power = (data.power / 2)
        data.presision += 1
    else:
        power = EventModel(power, date)
    db.session.add(power)
    db.session.commit()
