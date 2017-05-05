from ... import BaseModel, PayloadSplitter, DataDescriptor, ClassInfo
zalm = {'06' : 'AccessControl'}
icons = {'AccessControl' : {'16' : 'fa fa-bell', '17' : 'fa fa-bell-slash-o',\
         '1' : 'fa fa-bell', '0' : 'fa fa-bell-slash-o'}}

class AlarmModel:
    v1alm = DataDescriptor('v1alm')
    zalm = DataDescriptor('zalm')
    evt = DataDescriptor('evt')
    level = DataDescriptor('level')
    exValid = DataDescriptor('exValid')
    srcNode = DataDescriptor('srcNode')
    stat = DataDescriptor('stat')
    evtType = DataDescriptor('evtType')
    
    def __init__(self):
        self.v1alm = None
        self.zalm = None
        self.evt = None
        self.level = None
        self.exValid = None
        self.srcNode = None
        self.stat = None
        self.evtType = None
        super().__init__()


def Info(classtype = None):
    classinfo = ClassInfo()
    classinfo.classname = 'alarm'
    classinfo.classnumber = '71'
    classinfo.types = True
    classinfo.fields = []
    if classtype:
        try:
            classinfo.fields.append(eval(zalm[classtype] + '.Fields')())
        except KeyError as e:
            print("Unable to add {} for class {}".format(classtype,
                                                         classinfo.classname))
    return classinfo


def Icon(value, classtype):
    return icons[classtype][value]

def Load():
    return {'notification': None}

@PayloadSplitter(model=AlarmModel)
def Event(payload):
    try:
        return eval(zalm[payload.zalm] + '.Event')(payload)
    except KeyError as e:
        print(str(e))

from . import AccessControl
