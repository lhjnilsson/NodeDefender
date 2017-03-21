from . import parser

def enabled():
    return parser['LOGGING']['ENABLED']

def type():
    return parser['LOGGING']['TYPE']

def name():
    return parser['LOGGING']['NAME']

def server():
    return parser['LOGGING']['SERVER']

def port():
    return parser['LOGGING']['PORT']

