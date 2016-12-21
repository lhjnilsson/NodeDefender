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

def DeleteNode():
    pass

