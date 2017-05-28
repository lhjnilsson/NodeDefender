from ... import BaseModel, PayloadSplitter, DataDescriptor
from .. import ClassInfo

zalm = {'06' : 'AccessControl'}
icons = {'AccessControl' : {'16' : 'fa fa-bell', '17' : 'fa fa-bell-slash-o',\
         '1' : 'fa fa-bell', '0' : 'fa fa-bell-slash-o'}}

class AlarmModel:
    v1alm = DataDescriptor('v1alm')
    zalm = DataDescriptor('zalm')
    evt = DataDescriptor('evt')
    level = DataDescriptor('level')
    exValid = DataDescriptor('exValid')
    srcNode = DataDescriptor('srcNode')
    stat = DataDescriptor('stat')
    evtType = DataDescriptor('evtType')
    
    def __init__(self):
        self.v1alm = None
        self.zalm = None
        self.evt = None
        self.level = None
        self.exValid = None
        self.srcNode = None
        self.stat = None
        self.evtType = None
        super().__init__()


def Info(cctype = None):
    if cctype:
        return eval(zalm[cctype] + '.Info')
    classinfo = ClassInfo()
    classinfo.number = '71'
    classinfo.name = 'alarm'
    classinfo.types = True
    return classinfo


def Icon(value, cctype):
    try:
        return icons[cctype][value]
    except KeyError:
        try:
            icons[zalm[cctype]][value]
        except KeyError as e:
            raise KeyError(e)

def Load():
    return {'notification': None}

def Fields():
    return False

@PayloadSplitter(model=AlarmModel)
def Event(payload):
    payload.cc = '71'
    payload.ccname = 'alarm'
    try:
        payload.cctype = payload.zalm
        return eval(zalm[payload.zalm] + '.Event')(payload)
    except KeyError as e:
        print(str(e))

from . import AccessControl
