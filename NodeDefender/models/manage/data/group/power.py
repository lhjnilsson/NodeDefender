from datetime import datetime, timedelta
from ... import group as GroupModel
from ... import data

def Get(group, to_date = datetime.now(), from_date = (datetime.now() -
                                                      timedelta(days=7))):
    group = GroupModel.Get(group)
    return [data.node.heat(node, to_date, from_date) for node in group.nodes]
