from ... import BaseModel, PayloadSplitter, DataDescriptor

zalm = {'06' : 'AccessControl'}

class AlarmModel(BaseModel):
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


def Info():
    return 'alarm', True

def Load():
    return {'notification': None}

@PayloadSplitter(model=AlarmModel)
def Event(payload):
    try:
        return eval(zalm[payload.zalm] + '.Event')(payload)
    except NameError as e:
        print(kwargs['zalm'], e)

from . import AccessControl
