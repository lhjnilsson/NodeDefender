from ....SQL import EventModel, GroupModel, NodeModel
from ..... import db
from sqlalchemy import or_

def Average(*groups, time_ago = None):
    if time_ago is None:
        time_ago = (datetime.now() - timedelta(days=1))

    groups = db.session.query(GroupModel).\
            filter(GroupModel.name.in_(*[groups])).first()

    ret_data = []
    for group in groups:
        group_data = {}

        icpes = [node.icpe.macaddr for node in group.nodes]

        total_events = db.session.query(EventModel).\
                join(EventModel.icpe).\
                filter(iCPEModel.macaddr.in_(*[icpes])).\
                filter(EventModel.date > time_ago).all()

        group_data['group'] = group.name
        group_data['total'] = len(total_events)
        group_data['critical'] = len([event for event in total_events if
                                event.critical])
        group_data['normal'] = len([event for event in total_events if
                              event.normal])
        ret_data.append(group_data)

    return group_data

def Latest(group):
    return EventModel.query.join(NodeModel).\
            filter(NodeModel.groups.any(GroupModel.name == group)).first()

def Get(group, limit = 20):
    group = GroupModel.query.filter(GroupModel.name == group).first()
    if not group:
        return False
    return EventModel.query.join(NodeModel).\
            filter(NodeModel.name.in_([node.name for node in group.nodes])).\
            order_by(EventModel.date.desc()).limit(int(limit)).all()

