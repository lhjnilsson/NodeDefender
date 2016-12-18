from configparser import ConfigParser


'''
Utilities used to read and modify configuration
'''
config = ConfigParser()

def ReadConf(section):
    config.read('settings.ini')
    for key, value in config[section].items():
        yield key, value


def ReadBackup():
    pass

def SetBackup():
    pass

def ReadMqtt():
    mqttconf = []
    for value in range(4):
        mqttconf.append({key: value for key, value in\
                         ReadConf('MQTT'+str(value + 1))})
    return mqttconf

def SetMqtt():
    pass

def ReadServer():
    Settings = {}
    Settings['BASE'] = {key: value for key, value in ReadConf('BASE')}
    Settings['SNMP'] = {key: value for key, value in ReadConf('SNMP')}
    Settings['MAIL'] = {key: value for key, value in ReadConf('MAIL')}
    Settings['DATABASE'] = {key: value for key, value in ReadConf('DATABASE')}
    return Settings

def SetServer():
    pass

def ReadUsers():
    pass

def SetUsers():
    pass

