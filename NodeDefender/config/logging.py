import NodeDefender

enabled = False
level = "debug"
logging_type = "local"
logging_filepath = "/tmp/nodedefender.log"
logging_host = "127.0.0.1"
logging_port = 514

def load_config(parser):
    global enabled
    global level
    global logging_type
    global logging_filepath
    global logging_host
    global logging_port
    
    enabled = True if parser['LOGGING']['ENABLED'] == 'True' else False



def enabled():
    return True if NodeDefender.config.parser['LOGGING']['ENABLED'] == 'True' else False

def level():
    return NodeDefender.config.parser['LOGGING']['LEVEL']

def type():
    return NodeDefender.config.parser['LOGGING']['TYPE']

def name():
    return NodeDefender.config.parser['LOGGING']['FILEPATH']

def server():
    return NodeDefender.config.parser['LOGGING']['SERVER']

def port():
    return NodeDefender.config.parser['LOGGING']['PORT']

def get_cfg(key):
    return NodeDefender.config.parser['LOGGING'][key]

def set_cfg(**kwargs):
    for key, value in kwargs.items():
        NodeDefender.config.parser['LOGGING'][key] = str(value)

    return NodeDefender.config.write()
