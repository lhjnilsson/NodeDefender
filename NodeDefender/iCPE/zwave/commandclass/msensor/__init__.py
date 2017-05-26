from ... import BaseModel, PayloadSplitter, DataDescriptor, ClassInfo

mtype = {'1' : 'AirTemperature', '0x01' : 'AirTemperature'}

class MsensorModel:
    unit = DataDescriptor('unit')
    type = DataDescriptor('type')
    precision = DataDescriptor('precision')
    size = DataDescriptor('sizeize')
    data32 = DataDescriptor('data32')
    data = DataDescriptor('data')

    def __init__(self):
        self.unit = None
        self.type = None
        self.precision = None
        self.size = None
        self.data32 = None
        self.data = None
        super().__init__()

def Info(classtype = None):
    classinfo = ClassInfo()
    classinfo.cc = '31'
    classinfo.ccname = 'msensor'
    classinfo.types = True
    classinfo.datafields = None
    if classtype:
        try:
            classinfo.fields.append(eval(mtype[classtype] + '.Fields')())
        except KeyError:
            print("Unable to add {} for class {}".format(classtype,
                                                         classinfo.clasname))
    return classinfo

def Load(classtypes):
    return {'meter' : 0}

@PayloadSplitter(model=MsensorModel)
def Event(payload):
    try:
        return eval(mtype[payload.type] + '.Event')(payload)
    except KeyError as e:
        print(str(e))

from . import AirTemperature
