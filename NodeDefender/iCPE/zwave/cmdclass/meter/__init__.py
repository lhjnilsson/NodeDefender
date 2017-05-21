from ... import BaseModel, PayloadSplitter, DataDescriptor, ClassInfo

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

def Info(cctype = None):
    classinfo = ClassInfo()
    classinfo.cc = '25'
    classinfo.ccname = 'meter'
    classinfo.cctypes = True
    classinfo.datafield = None
    if cctype:
        try:
            classinfo.datafield = (eval(mtype[cctype] + '.Datafield')())
        except KeyError:
            print("Unable to add {} for class {}".format(cctype,
                                                         classinfo.clasname))
    return classinfo

def Icon(value, cctype):
    return icons[cctype]

def Load(classtypes):
    return {'meter' : 0}

@PayloadSplitter(model=MeterModel)
def Event(payload):
    try:
        return eval(mtype[payload.type] + '.Event')(payload)
    except KeyError as e:
        print(str(e))

from . import Electric
