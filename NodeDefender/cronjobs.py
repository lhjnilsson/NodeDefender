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
from itertools import groupby
from .models import iCPEModel, NodeHeatStatModel, NodePowerStatModel, \
        NodeHeatModel, NodePowerModel
from . import db

def GetHeatEvents():
    events = NodeHeatModel.query.all()
    return events

def GetPowerEvents():
    events = NodePowerModel.query.all()
    return events

def ProcessEvents(icpe, nodeid, events, datatype):
    EventDict = dict((k, list(g)) for k, g in \
                     groupby(events, lambda event: event.created_on.year))

    for year, events in EventDict.items():
        EventDict[year] = dict((k, list(g)) for k, g in \
                              groupby(events, lambda event:
                                      event.created_on.month))
        for month, events in EventDict[year].items():
            EventDict[year][month] = dict((k, list(g)) for k, g in \
                                        groupby(events, lambda event: \
                                                event.created_on.day))
            for day, events in EventDict[year][month].items():
                EventDict[year][month][day] = dict((k, list(g)) for k, g in \
                                                  groupby(events, lambda event:\
                                                          event.created_on.hour))
                for hour, events in EventDict[year][month][day].items():
                    eval('Insert'+datatype)(icpe, nodeid, EventDict[year][month][day][hour])

def InsertHeat(icpe, nodeid, events):
    numEvents = 0
    totalHeat = 0.0
    date = events[0].created_on.replace(minute=0, second=0, microsecond=0)
    for event in events:
        totalHeat += event.heat
        numEvents += 1
    AvarageHeat = totalHeat / numEvents
    HeatStatModel = NodeHeatStatModel.query.filter_by(date = date).first()
    if HeatStatModel is None:
        HeatStatModel = NodeHeatStatModel(nodeid, numEvents, AvarageHeat, date)
    else:
        CurrentHeat = HeatStatModel.heat
        HeatStatModel.heat = (CurrentHeat + AvarageHeat) / 2
        HeatStatModel.events += numEvents
    icpe = iCPEModel.query.filter_by(mac = icpe).first()
    if icpe is None:
        print('NOT FOUND ICPE')
        return
    icpe.heatstat.append(HeatStatModel)
    db.session.add(icpe)
    db.session.commit()

def InsertPower(icpe, nodeid, events):
    numEvents = 0
    totalPower = 0.0
    date = events[0].created_on.replace(minute=0, second=0, microsecond=0)
    for event in events:
        totalPower += event.power
        numEvents += 1
    AvaragePower = totalPower / numEvents
    PowerStatModel = NodePowerStatModel.query.filter_by(date = date).first()
    if PowerStatModel is None:
        PowerStatModel = NodePowerStatModel(nodeid, numEvents, AvaragePower, date)
    else:
        CurrentPower = PowerStatModel.power
        PowerStatModel.Power = (CurrentPower + AvaragePower) / 2
        PowerStatModel.events += numEvents
    icpe = iCPEModel.query.filter_by(mac = icpe).first()
    if icpe is None:
        print('NOT FOUND ICPE')
        return
    icpe.powerstat.append(PowerStatModel)
    db.session.add(icpe)
    db.session.commit()

def StatTask():
    # Process HeatEvents to by Hour
    heatevents = GetHeatEvents()
    if heatevents is None:
        pass
    else:
        HeatEvents = dict((k, list(g)) for k,g in groupby(heatevents, lambda
                                                          event:
                                                          event.parent.mac))
        for icpe, events in HeatEvents.items():
            HeatEvents[icpe] = dict((k, list(g)) \
                                    for k,g in groupby(events, lambda event:\
                                                       event.nodeid))
            for nodeid, events in HeatEvents[icpe].items():
                ProcessEvents(icpe, nodeid, HeatEvents[icpe][nodeid], 'Heat')
    # Process PowerEvents to by Hour
    powerevents = GetPowerEvents()
    if powerevents is None:
        pass
    else:
        PowerEvents = dict((k, list(g)) for k,g in groupby(powerevents, lambda
                                                          event:
                                                          event.parent.mac))
        for icpe, events in PowerEvents.items():
            PowerEvents[icpe] = dict((k, list(g)) \
                                     for k,g in groupby(events, lambda event:\
                                                       event.nodeid))
            for nodeid, events in PowerEvents[icpe].items():
                ProcessEvents(icpe, nodeid, PowerEvents[icpe][nodeid], 'Power')

    for event in heatevents:
        db.session.delete(event)
    for event in powerevents:
        db.session.delete(event)
    db.session.commit()