from functools import wraps
from ..manage import icpe as iCPESQL
from ..manage import sensor as SensorSQL
from ..manage import commandclass as CommandclassSQL

def LookupiCPE(func):
    @wraps(func)
    def wrapper(icpe):
        if type(icpe) is str:
            return func(iCPESQL.Get(icpe))
        else:
            return func(icpe)
    return wrapper

def LookupSensor(func):
    @wraps(func)
    def wrapper(icpe, sensor = None):
        if type(icpe) is str:
            return func(SensorSQL.Get(icpe, sensor))
        else:
            return func(icpe)
    return wrapper

def LookupCommandclass(func):
    @wraps(func)
    def wrapper(icpe, sensor = None, commandclass = None):
        if type(icpe) is str:
            return func(CommandclassSQL.Get(icpe, sensor, commandclass))
        else:
            return func(icpe)
    return wrapper
