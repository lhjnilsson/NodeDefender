from functools import wraps
from .. import db

def VerifyiCPE(func):
    @wraps(func)
    def wrapper(topic, payload, mqttsrc):
        db.icpe.Verify(topic, payload, mqttsrc)
        return func(topic, payload, mqttsrc)
    return wrapper

def VerifySensor(func):
    @wraps(func)
    def wrapper(topic, payload, mqttsrc):
        db.sensor.Verify(topic, payload, mqttsrc)
        return func(topic, payload, mqttsrc)
    return wrapper

def VerifyCmdclass(func):
    @wraps(func)
    def wrapper(topic, payload, mqttsrc):
        db.cmdclass.Verify(topic, payload, mqttsrc)
        return func(topic, payload, mqttsrc)
    return wrapper

