from ... import PayloadSplitter, DataDescriptor, ClassInfo

icons = {True : 'fa fa-toggle-on', False : 'fa fa-toggle-off'}

class BasicModel:
    value = DataDescriptor('value')

    def __init__(self):
        self.value = None
        super().__init__()


def Info():
    classinfo = ClassInfo()
    classinfo.cc = '25'
    classinfo.ccname = 'bswitch'
    classinfo.cctypes = False
    return classinfo

def Fields():
    return {'type' : 'switch', 'readonly' : False, 'name' : 'Switch'}
 
def Load(classtypes):
    return {'bswitch' : None}

def Icon(value, classtype):
    return icons[eval(value)]

@PayloadSplitter(model=BasicModel)
def Event(payload):
    payload.ccevent = 'Switch'
    if payload.value == '0':
        payload.value = False
    
    else:
        payload.value = True

    return payload
