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

def GetNode(user, group, node):
    pass

def NodeList(user, group = None):
    if type(user) is str:
            user = UserModel.query.filter_by(email = email).first()
            if user is None:
                raise KeyError('Cant find user in database')
    if group:
        groupmap = {}
        for group in user.groups:
            groupmap[group] = [node for node in group.nodes]

        return groupmap
    else:
        if type(group) is str:
            group = GroupModel.query.filter_by(name=group).first()
            if group is None:
                raise KeyError('Cant find group in Database')
            if user not in group.users:
                raise KeyError('User not authorized to view Node')
        return [node for node in group.nodes]

def CreateiCPE(mac):
    pass

def DeleteiCPE(mac):
    pass

