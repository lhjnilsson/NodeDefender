from ..SQL import GroupModel, NodeModel, iCPEModel, SensorModel, UserModel

def Group(name):
    return GroupModel.query.filter_by(name = name).first().statistics

def Node(name):
    return NodeModel.query.filter_by(name = name).first().statistics

def iCPE(name):
    return iCPEModel.query.filter_by(name = name).first().statistics

def Sensor(name):
    return SensorModel.query.filter_by(name = name).first().statistics

def Set():
    pass

def Get(email):
    data = {}
    user = UserModel.query.filter_by(email = email).first()
    if Group:
        for group in user.groups:
            data[group.name] = group.statistics
    return data
