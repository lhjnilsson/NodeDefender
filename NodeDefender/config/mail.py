from . import parser

def enabled():
    return parser['MAIL']['ENABLED']

def server():
    return parser['MAIL']['SERVER']

def port():
    return parser['MAIL']['PORT']

def tls():
    return parser['MAIL']['TLS']

def ssl():
    return parser['MAIL']['SSL']

def username():
    return parser['MAIL']['USERNAME']

def password():
    return parser['MAIL']['PASSWORD']
