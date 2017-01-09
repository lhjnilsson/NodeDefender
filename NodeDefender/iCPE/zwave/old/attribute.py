from ... import outSocketQueue
from ... import NodeLogQueue

class Attribute:
    def __init__(self, name, datatype, unit = None):
        self.name = name
        self.datatype = datatype
        self.unit = unit # e.g. Celsius or Watt

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            try:
                return instance.__dict__[self.name]
            except KeyError:
                return None

    def __set__(self, instance, value):
        if not isinstance(value, self.datatype):
            raise TypeError('Expceted an ', self.datatype)
        mac = instance.__dict__['mac']
        nodeid = instance.__dict__['nodeid']
        Alias = instance.__dict__['Alias']
        # print('---setting: ', mac, nodeid, self.name, value)
        msg = {'nodeid' : nodeid, 'mac' : mac, 'attribute' : self.name, 'value' :
               value, 'Alias' : Alias, 'datatype' : str(self.datatype)}
        outSocketQueue.put(('roomevent', msg, mac))
        NodeLogQueue.put((self.unit, msg))
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        raise TypeError('You cannot delete me.')
