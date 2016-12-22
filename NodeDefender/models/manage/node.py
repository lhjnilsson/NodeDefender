from ..SQL import GroupModel, NodeModel

def Create(node, group):
    if type(group) is str:
        group = GroupModel.query.filter_by(name = group).first()
        if group is None:
            raise LookupError('Cant find group')

    node = NodeModel(node, group)
    db.session.commit()
    return node

def Delete(node):
    if type(node) is str:
        node = NodeModel.query.filter_by(name = node).first()
        if node is None:
            raise LookupError('Cant find node')

    db.session.delete(node)
    db.session.commit()
    return node

def Join(node, group):
    if type(node) is str:
        node = NodeModel.query.filter_by(alias = node).first()
        if node is None:
            raise LookupError('Cant find node')

    if type(group) is str:
        group = GroupModel.query.filter_by(name = group).first()
        if group is None:
            raise LookupError('Cant find group')

    node.groups.append(group)
    db.session.add(node)
    db.session.commit()
    return node

def Leave(node, group):
    if type(node) is str:
        node = NodeModel.query.filter_by(alias = node).first()
        if node is None:
            raise LookupError('Cant find node')

    if type(group) is str:
        group = GroupModel.query.filter_by(name = group).first()
        if group is None:
            raise LookupError('Cant find group')

    node.nodes.remove(group)
    db.session.add(node)
    db.session.commit()
    return node

def Get(node):
    if type(node) is str:
        node = NodeModel.query.filter_by(name = node).first()
        if node is None:
            raise LookupError('cant find node')
    return node

def List():
    return [node for node in NodeModel.query.all()]


def Groups(node):
    if type(node) is str:
        node = NodeModel.query.filter_by(name = node).first()
        if node is None:
            raise LookupError('Cant find node')
    
    return [group for group in node.groups]

def iCPEs(node):
    if type(node) is str:
        node = NodeModel.query.filter_by(name = node).first()
        if node is None:
            raise LookupError('Cant fine node')

    return [icpe for icpe in node.icpes]
