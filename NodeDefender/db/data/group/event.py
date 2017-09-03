from NodeDefender.db.sql import SQL, EventModel, GroupModel, NodeModel, iCPEModel
from datetime import datetime, timedelta
from sqlalchemy import or_

def average(group, time_ago = None):
    if time_ago is None:
        time_ago = (datetime.now() - timedelta(days=1))

    group = SQL.session.query(GroupModel).filter(GroupModel.name == group).first()
    if group is None:
        return False

    icpes = [node.icpe.macaddr for node in group.nodes if node.icpe]

    total_events = SQL.session.query(EventModel).\
            join(EventModel.icpe).\
            filter(iCPEModel.macaddr.in_(*[icpes])).\
            filter(EventModel.date > time_ago).all()

    ret_data = {}
    ret_data['name'] = group.name
    ret_data['total'] = len(total_events)
    ret_data['critical'] = len([event for event in total_events if
                                event.critical])
    ret_data['normal'] = len([event for event in total_events if
                              event.normal])
    return ret_data


def latest(group):
    return EventModel.query.join(NodeModel).\
            filter(NodeModel.groups.any(GroupModel.name == group)).first()

def list(group, limit = 20):
    group = GroupModel.query.filter(GroupModel.name == group).first()
    if not group:
        return False
    return EventModel.query.join(NodeModel).\
            filter(NodeModel.name.in_([node.name for node in group.nodes])).\
            order_by(EventModel.date.desc()).limit(int(limit)).all()

