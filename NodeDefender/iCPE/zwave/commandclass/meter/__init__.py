from ... import BaseModel, PayloadSplitter, DataDescriptor
from .. import ClassInfo

mtype = {'1' : 'Electric'}
icons = {'Electric' : 'fa fa-plug'}

class MeterModel:
    unit = DataDescriptor('unit')
    type = DataDescriptor('type')
    precision = DataDescriptor('precision')
    dataSize = DataDescriptor('dataSize')
    data32 = DataDescriptor('data32')
    deltaTime = DataDescriptor('deltaTime')
    data = DataDescriptor('data')
    prevData = DataDescriptor('prevData')
    rateType = DataDescriptor('rateType')

    def __init__(self):
        self.unit = None
        self.type = None
        self.precision = None
        self.dataSize = None
        self.data32 = None
        self.deltaTime = None
        self.data = None
        self.prevData = None
        self.rateType = None
        super().__init__()

def Info(classtype = None):
    if classtype:
        return eval(mgtype[classtype] + '.Info')()
    classinfo = ClassInfo()
    classinfo.number = '25'
    classinfo.name = 'meter'
    classinfo.types = True
    return classinfo

def Icon(value, cctype):
    return icons[cctype]

def Load(classtypes):
    return {'meter' : 0}

def Fields():
    return False

@PayloadSplitter(model=MeterModel)
def Event(payload):
    try:
        return eval(mtype[payload.type] + '.Event')(payload)
    except KeyError as e:
        print(str(e))

from . import Electric
