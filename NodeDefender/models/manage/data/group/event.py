from ....SQL import EventModel, GroupModel, NodeModel
from ..... import db
from sqlalchemy import or_

def Latest(group):
    return EventModel.query.join(NodeModel).\
            filter(NodeModel.groups.any(GroupModel.name == group)).first()

def Get(group, limit = 20):
    group = GroupModel.query.filter(GroupModel.name == group).first()
    if not group:
        return False
    return EventModel.query.join(NodeModel).\
            filter(NodeModel.name.in_([name for name in group.nodes])).\
            order_by(EventModel.date.desc()).limit(int(limit)).all()

