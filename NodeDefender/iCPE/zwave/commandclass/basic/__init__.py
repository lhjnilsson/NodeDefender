from ... import PayloadSplitter, DataDescriptor 
from .. import ClassInfo

icons = {True : 'fa fa-toggle-on', False : 'fa fa-toggle-off'}

class BasicModel:
    value = DataDescriptor('value')

    def __init__(self):
        self.value = None
        super().__init__()


def Info():
    classinfo = ClassInfo()
    classinfo.name = 'basic'
    classinfo.number = '20'
    classinfo.types = False
    return classinfo

def Fields():
    return {'type' : 'box', 'readonly' : True, 'name' : 'Basic'}

def Load(classtypes):
    return {'basic' : None}

def Icon(value):
    return icons[eval(value)]

@PayloadSplitter(model=BasicModel)
def Event(payload):
    payload.field = 'Basic'
    if payload.value == '0x00':
        payload.value = False
        payload.enabled = False
    else:
        payload.value = True
        payload.enabled = True

    return payload
