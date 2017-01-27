from functools import wraps
from ..manage import icpe as iCPESQL
from ..manage import sensor as SensorSQL
from ..manage import cmdclass as CmdclassSQL

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
        if type(icpe) is str and sensor:
            return func(SensorSQL.Get(icpe, sensor))
        else:
            return func(icpe)
    return wrapper

def LookupCmdclass(func):
    @wraps(func)
    def wrapper(icpe, sensor = None, cmdclass = None):
        if type(icpe) is str and sensor and cmdclass:
            return func(CmdclassSQL.Get(icpe, sensor, cmdclass))
        else:
            return func(icpe)
    return wrapper
