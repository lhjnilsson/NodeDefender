from .models import *
from . import db
from sqlalchemy import desc

def GetHourlyStat():
    Hourly = HourlyStatistics.query.first()
    if Hourly is not None:
        return Hourly
    else:
        return {'heat': 0.0, 'power' : 0.0, 'events' : 0}

def SetHourlyStat(heat, power, events):
    Hourly = HourlyStatistics.query.first()
    if Hourly is None:
        Hourly = HourlyStatistics(heat, power, events)
    else:
        Hourly.heat = heat
        Hourly.power = power
        Hourly.events = events
    db.session.add(Hourly)
    db.session.commit()

def GetDailyStat():
    Daily = DailyStatistics.query.first()
    if Daily is not None:
        return Daily
    else:
        return {'heat': 0.0, 'power' : 0.0, 'events' : 0}

def SetDailyStat(heat, power, events):
    Daily = DailyStatistics.query.first()
    if Daily is None:
        Daily = DailyStatistics(heat, power, events)
    else:
        Daily.heat = heat
        Daily.power = power
        Daily.events = events
    db.session.add(Daily)
    db.session.commit()

def GetHourlyLog():
    HourlyLog = \
    HourlylogStatistics.query.order_by(desc(HourlylogStatistics.id)).limit(24)
    return HourlyLog

def SetHourlyLog(heat, power, events):
    HourlyLog = HourlylogStatistics(float(heat), float(power), int(events))
    db.session.add(HourlyLog)
    db.session.commit()
    return True

def GetDailyLog():
    DailyLog = \
    DailylogStatistics.query.order_by(desc(DailylogStatistics.id)).limit(24)
    return DailyLog

def SetDailyLog(heat, power, events):
    DailyLog = DailylogStatistics(heat, power, events)
    db.session.add(DailyLog)
    db.session.commit()
    return True

def GetAllStats():
    Hourly = GetHourlyStat()
    Daily = GetDailyStat()
    return {'daily' : Daily, 'hourly' : Hourly}
