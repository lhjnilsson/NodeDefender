from .attribute import Attribute
from threading import Thread
from time import sleep

class c0071:
    '''
    Alarm Command class
    '''
    Door = Attribute('Door', bool)
    def __init__(self):
        self.WebForm['fields'].append({'class' : 'Door', 'type' : 'checkbox',
                                       'value' : False, 'readonly' : False})
        self.Door = False # Dont know how to send and get intial value, will
                           # change this later
        super().__init__()

    def WSDoor(self, **kwargs):
        pass

    def c0x0071(self, topic, payload):
        getattr(self, 'evt'+payload['evt'])(topic, payload)

    def evt16(self, topic, payload):
        self.Door = True
        return 'open'

    def evt17(self, topic, payload):
        self.Door = False
        return 'closed'

class c0020:
    '''
    Basic Command class
    '''
    Basic = Attribute('Basic', bool)
    def __init__(self):
        self.WebForm['fields'].append({'class' : 'Basic', 'type': 'checkbox', 'value' :
                                       False, 'readonly' : False})
        self.MQTT.put(('icpe/0x'+self.mac+'/cmd/node/'+self.nodeid+'/class/basic/act/get',
                       '')) # To know the current state
        super().__init__()

    def c0x0020(self, topic, payload):
        return getattr(self, 'value'+payload['value'][:-1])()

    def value0xff(self):
        self.Basic = True
        return 'lights', 'on'

    def value0x00(self):
        self.Basic = False
        return 'lights', 'off'

    def WSBasic(self, **kwargs):
        print(kwargs)
        getattr(self, 'State'+str(kwargs['state']))(**kwargs)

    def StateTrue(self, **kwargs):
        self.Basic = True
        topic = 'icpe/0x{}/cmd/node/{}/class/basic/act/set'\
                .format(kwargs['mac'], kwargs['nodeid'])
        payload = '0xff'
        self.MQTT.put((topic, payload))
        return True

    def StateFalse(self, **kwargs):
        self.Basic = False
        topic = 'icpe/0x{}/cmd/node/{}/class/basic/act/set'\
                .format(kwargs['mac'], kwargs['nodeid'])
        payload = '0x00'
        self.MQTT.put((topic, payload))
        return True

class c0025:
    def __init__(self):
        print('0025')
        super().__init__()

    def c0x0025(self, topic, payload):
        pass

class c0031:
    Celsius = Attribute('Celsius', float, 'Celsius')

    def __init__(self):
        self.WebForm['fields'].append({'class' : 'Celsius', 'type': 'value',
                                      'value' : 0.00, 'readonly' : True})
        super().__init__()
    
    def c0x0031(self, topic, payload):
        try:
            getattr(self, payload['descr'] + payload['type'])(topic, payload)
        except AttributeError:
            print('0031',payload['desc'], payload['type'])

    def msensor0x01(self, topic, payload):
        self.Celsius = int(payload['data'], 0) / 10

class c0032:
    Watt = Attribute('Watt', float, 'Watt')
    def __init__(self):
        self.WebForm['fields'].append({'class' : 'Watt', 'type': 'value', 'value' :
                                       0.00, 'readonly' : True}) 
        _t1 = Thread(target=self._CheckPower,)
        _t1.start()
        super().__init__()
    
    def c0x0032(self, topic, payload):
        self.Watt = int(payload['data'], 0) / 10

    def _CheckPower(self):
        while True:
            topic = 'icpe/0x'+self.mac+'/cmd/node/'+self.nodeid+'/class/meter/act/get'
            payload = '2'
            self.MQTT.put((topic, payload))
            sleep(10)

class c0073:
    def __init__(self):
        print('0073')
        super().__init__()

    def infopower(self, payload):
        print('pwoer is' ,payload['level'])

    def c0x0073(self, topic, payload):
        return getattr(self, 'info'+payload['descr'])(payload)
