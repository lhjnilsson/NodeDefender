from .. import DataDescriptor

class ClassInfo:
    name = DataDescriptor('name')
    number = DataDescriptor('number')
    types = DataDescriptor('types')
    fields = DataDescriptor('fields')

    def __init__(self):
        self.name = None
        self.number = None
        self.types = None
        self.fields = False

class ClassTypeInfo:
    name = DataDescriptor('name')
    number = DataDescriptor('number')
    fields = DataDescriptor('fields')

    def __init__(self):
        self.name = None
        self.number = None
        self.fields = False

from . import alarm
from . import basic
from . import bswitch
from . import meter
from . import msensor
