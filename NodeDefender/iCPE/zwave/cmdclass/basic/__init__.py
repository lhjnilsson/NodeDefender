from ... import PayloadSplitter, DataDescriptor, ClassInfo

icons = {True : 'fa fa-toggle-on', False : 'fa fa-toggle-off'}

class BasicModel:
    value = DataDescriptor('value')

    def __init__(self):
        self.value = None
        super().__init__()


def Info():
    classinfo = ClassInfo()
    classinfo.classname = 'basic'
    classinfo.classnumber = '20'
    classinfo.types = False
    classinfo.fields = [{'type' : 'switch', 'readonly' : False, 'name' :
                            'basic'}]
    return classinfo

def Load(classtypes):
    return {'basic' : None}

def Icon(value, classtype):
    return icons[eval(value)]

@PayloadSplitter(model=BasicModel)
def Event(payload):
    payload.name = 'basic'
    if payload.value == '0x00':
        payload.value = False
        payload.enabled = False
    else:
        payload.value = True
        payload.enabled = True

    return payload
