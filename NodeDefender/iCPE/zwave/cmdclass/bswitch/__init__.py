from ... import PayloadSplitter, DataDescriptor, ClassInfo

icons = {True : 'fa fa-toggle-on', False : 'fa fa-toggle-off'}

class BasicModel:
    value = DataDescriptor('value')

    def __init__(self):
        self.value = None
        super().__init__()


def Info():
    classinfo = ClassInfo()
    classinfo.classname = 'bswitch'
    classinfo.classnumber = '25'
    classinfo.types = False
    classinfo.fields = [{'type' : 'switch', 'readonly' : False, 'name' :
                            'Switch'}]
    return classinfo

def Load(classtypes):
    return {'bswitch' : None}

def Icon(value, classtype):
    return icons[eval(value)]

@PayloadSplitter(model=BasicModel)
def Event(payload):
    payload.name = 'bswitch'
    if payload.value == '0':
        payload.value = False
        payload.enabled = False
    else:
        payload.value = True
        payload.enabled = True

    return payload
