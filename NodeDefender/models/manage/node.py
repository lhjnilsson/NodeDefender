from ..SQL import UserModel, GroupModel, NodeModel

def Get(node):
    if type(node) is str:
        node = NodeModel.query.filter_by(name = node).first()
        if node is None:
            raise LookupError('cant find node')
    return node

def List():
    return [node for node in NodeModel.query.all()]

def Delete(node):
    if type(node) is str:
        node = NodeModel.query.filter_by(name = node).first()
        if node is None:
            raise LookupError('Cant find node')

    db.session.delete(node)
    db.session.commit()
    return node

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
