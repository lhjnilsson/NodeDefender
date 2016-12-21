def GetiCPE(user, group, mac):
    if type(user) is str:
        user = UserModel.query.filter_by(email = email).first()
        if user is None:
            raise KeyError('Cant find user in Database')

    if type(group) is str:
        group = GroupModel.query.filter_by(name = name).first()
        if group is None:
            raise KeyError('Cant find group in Database')

    iCPE = iCPEModel.query.filter_by(mac = mac).first()
    if iCPE.node not in group.nodes:
        raise KeyError('iCPE is not a part of Group')

    if usernot in group.users:
        raise KeyError('User not Authorized to view this iCPE')

    return iCPE

def CreateiCPE(user, mac, node = None):
    pass

def DeleteiCPE(icpe):
    if type(icpe) is str:
        icpe = iCPEModel.query.filter_by(mac = mac).first()
        if icpe is None:
            raise KeyError('Cant find iCPE in Database')
        
    db.session.delete(icpe)
    db.session.commi()
    return icpe
