from ... import BaseModel, PayloadSplitter, DataDescriptor, ClassInfo

class BasicModel(BaseModel):
    value = DataDescriptor('value')

    def __init__(self):
        self.value = None
        super().__init__()


def Info():
    classinfo = ClassInfo()
    classinfo.classname = 'basic'
    classinfo.classnumber = '20'
    classinfo.types = False
    classinfo.fields = [{'type' : 'checkbox', 'readonly' : False, 'name' :
                            'basic'}]
    return classinfo

def Load(classtypes):
    return {'basic' : None}

@PayloadSplitter(model=BasicModel)
def Event(payload):
    if payload.value == '0x00':
        payload._retdata['basic'] = False
    else:
        payload._retdata['basic'] = True

    return payload
