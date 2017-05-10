from datetime import datetime, timedelta
from ....SQL import EventModel, NodeModel
from ..... import db
from sqlalchemy import or_, desc


def Latest(node):
    return EventModel.query.filter_by(name = node).first()

def Get(node, from_date = None, to_date = None, limit = None):

    if from_date == None:
        from_date = (datetime.now() - timedelta(days = 7))
    
    if to_date == None:
        to_date = datetime.now()

    if limit == None:
        limit = 10

    return db.session.query(EventModel).join(EventModel.node).\
            filter(NodeModel.name == node).\
            filter(EventModel.date > from_date, EventModel.date < to_date).\
            order_by(EventModel.date.desc()).limit(limit).all()

def Put(node, power, date):
    data = session.query(EventModel).filter(name == node, date == date)
    if data:
        power = (data.power / 2)
        data.presision += 1
    else:
        power = EventModel(power, date)
    db.session.add(power)
    db.session.commit()
