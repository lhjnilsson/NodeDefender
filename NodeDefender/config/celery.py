from . import parser

def enabled():
    return parser['CELERY']['ENABLED']

def broker():
    return parser['CELERY']['BROKER']

def server():
    return parser['CELERY']['SERVER']

def port():
    return parser['CELERY']['PORT']

def database():
    return parser['CELERY']['DATABASE']

