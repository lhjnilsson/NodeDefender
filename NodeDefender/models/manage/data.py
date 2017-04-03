from ..SQL import GroupModel, NodeModel, iCPEModel, SensorModel, UserModel
from datetime import datetime, timedelta

def Group(name):
    return GroupModel.query.filter_by(name = name).first()

def Node(name):
    return NodeModel.query.filter_by(name = name).first()

def iCPE(name):
    return iCPEModel.query.filter_by(name = name).first()

def Sensor(name):
    return SensorModel.query.filter_by(name = name).first()

def Set():
    pass

def Get(email):
    return []


def Heat(group = None, node = None, icpe = None, sensor = None, fr = None, to =
         datetime.now()):
    if fr = None:
        fr = (datetime.now() - timedelta(days = 7))

