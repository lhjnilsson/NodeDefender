'''
Copyright (c) 2016 Connection Technology Systems Northern Europe

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE
SOFTWARE.
'''
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

