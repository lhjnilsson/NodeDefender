from configparser import ConfigParser
from .models.manage import mqtt as MQTTSQL
import os
from datetime import datetime
'''
Utilities used to read and modify configuration
'''
config = ConfigParser()


hostname = os.uname().nodename
release = 'Alpha-2'
_loaded_at = datetime.now()

def uptime():
    return str(datetime.now() - _loaded_at)

def general_info():
    hostname = os.uname().nodename
    

def ReadConf(section):
    config.read('settings.ini')
    for key, value in config[section].items():
        yield key, value


def ReadBackup():
    pass

def SetBackup():
    pass

def mqtt_list():
    mqttconf = []
    for value in range(4):
        mqttconf.append({key: value for key, value in\
                         ReadConf('MQTT'+str(value + 1))})
    return mqttconf

def get_mqtt():
    pass

def set_mqtt():
    pass

def read_server():
    s = {}
    return 
    s['BASE'] = {key: value for key, value in ReadConf('BASE')}
    s['SNMP'] = {key: value for key, value in ReadConf('SNMP')}
    s['MAIL'] = {key: value for key, value in ReadConf('MAIL')}
    s['DATABASE'] = {key: value for key, value in ReadConf('DATABASE')}
    return s

def set_server():
    pass


def read_database():
    pass

def set_database():
    pass
