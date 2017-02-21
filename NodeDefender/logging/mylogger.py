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
from threading import Thread
from . import NodeLogQueue, models, db
from .models import NodeEventModel, NodePowerModel, NodeHeatModel, iCPEModel

# For Font-awesome
FADict = {'BasicTrue' : 'toggle-on', 'BasicFalse' : 'toggle-off', 'AlarmTrue' :
          'Bell', 'AlarmFalse' : 'Bell-o', 'Power' : 'plug', 'Heat' : 'sun-o'}

def GetFA(key):
    try:
        return FADict[key]
    except KeyError:
        return 'question'

def ZWaveEvent(**kwargs):
    icpe = iCPEModel.query.filter_by(macaddr = kwargs['mac']).first()
    if not icpe:
        return
    FAIcon = GetFA(kwargs['attribute'] + str(kwargs['value']))
    event = NodeEventModel(kwargs['nodeid'], kwargs['Alias'], FAIcon)
    icpe.events.append(event)
    db.session.add(icpe)
    db.session.commit()

def PowerEvent(**kwargs):
    icpe = iCPEModel.query.filter_by(macaddr = kwargs['mac']).first()
    if icpe is None:
        return
    FAIcon = GetFA('Power')
    Power = NodePowerModel(kwargs['nodeid'], kwargs['value'], 'Watt', FAIcon)
    icpe.power.append(Power)
    db.session.add(icpe)
    db.session.commit()

def HeatEvent(**kwargs):
    icpe = iCPEModel.query.filter_by(macaddr = kwargs['mac']).first()
    if icpe is None:
        return
    FAIcon = GetFA('Heat')
    Heat = NodeHeatModel(kwargs['nodeid'], kwargs['value'], 'Celsuis', FAIcon)
    icpe.heat.append(Heat)
    db.session.add(icpe)
    db.session.commit()

def NodeLogger():
    while True:
        event, kwargs = NodeLogQueue.get()
        if event is None:
            ZWaveEvent(**kwargs)
        elif event.upper() == 'WATT':
            PowerEvent(**kwargs)
        elif event.upper() == 'CELSIUS':
            HeatEvent(**kwargs)
        else:
            print('got unknown logging event', event)

t1 = Thread(target = NodeLogger, )
t1.start()
