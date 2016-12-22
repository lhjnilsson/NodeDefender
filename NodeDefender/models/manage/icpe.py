from ..SQL import iCPEModel, NodeModel

def Create(mac, node):
    if type(node) is str:
        node = NodeModel.query.filter_by(name = Node).first()
        if node is None:
            raise LookupError('Node not found')

    icpe = iCPEModel(mac)
    node.icpes.append(icpe)
    db.session.add(node)
    db.session.commit()
    return icpe

def Delete(icpe):
    if type(icpe) is str:
        icpe = iCPEModel.query.filter_by(mac = icpe).first()

    db.session.delete(icpe)
    db.session.commit()

def Join(icpe, node):
    if type(icpe) is str:
        icpe = iCPEModel.query.filter_by(mac = icpe).first()
        if icpe is None:
            raise LookupError('iCPE not found')

    if type(Node) is str:
        node = GroupModel.query.filter_by(name = node).first()
        if node is None:
            raise LookupError('Node not found')

    group.icpes.append(icpe)
    db.session.add(group)
    db.session.commit()

def Leave(icpe, node):
    if type(icpe) is str:
        icpe = iCPEModel.query.filter_by(mac = icpe).first()
        if icpe is None:
            raise LookupError('iCPE not found')

    if type(group) is str:
        group = GroupModel.query.filter_by(name = group).first()
        if group is None:
            raise LookupError('Group not found')

    group.icpes.remove(icpe)
    db.session.add(group)
    db.session.commit()

def list():
    return [icpe for icpe in iCPEModel.query.all()]

def Get(icpe):
    return iCPEModel.query.filter_by(mac = icpe).first()
