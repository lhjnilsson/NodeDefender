from ... import BaseModel, PayloadSplitter, DataDescriptor

class BasicModel(BaseModel):
    value = DataDescriptor('value')

    def __init__(self):
        self.value = None
        super().__init__()


def Info():
    return 'basic', False, {'type' : 'checkbox', 'readonly' : False, 'name' :
                            'basic'}

def Load(classtypes):
    return {'basic' : None}

@PayloadSplitter(model=BasicModel)
def Event(payload):
    if payload.value == '0x00':
        payload._retdata['basic'] = False
    else:
        payload._retdata['basic'] = True

    return payload
