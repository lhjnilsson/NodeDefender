from ... import BaseModel, PayloadSplitter, DataDescriptor

mtype = {'1' : 'Electric'}

class MeterModel(BaseModel):
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

def Info():
    return 'meter', True

def Load(classtypes):
    return {'meter' : 0}

@PayloadSplitter(model=MeterModel)
def Event(payload):
    try:
        return eval(mtype[payload.type] + '.Event')(payload)
    except NameError as e:
        print(str(e))

from . import Electric
