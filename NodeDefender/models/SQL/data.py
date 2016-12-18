from ... import db


class Statistics(db.Model):
    __tablename__ = 'statistics'
    id = db.Column(db.Integer, primary_key=True)
    
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    group = db.relationship('GroupModel', backref='statistics')

    hourly = db.relationship('HourlyStatistics', backref="statistics")
    daily = db.relationship('DailyStatistics', backref='statistics')
    weekly = db.relationship('WeeklyStatistics', backref='statistics')
    
    def __init__(self):
        pass

'''
'''

class HourlyStatistics(db.Model):
    __tablename__ = 'hourlystatistics'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('statistics.id'))
    
    node = db.relationship('NodeModel', backref='hourlystatistics')
    icpe = db.relationship('iCPEModel', backref='hourlystatistics')
    zwavedevice = db.relationship('ZWaveDeviceModel',
                                  backref='hourlystatistics')

    heat = db.relationship('heatstat', backref='hourlystatistics')
    power = db.relationship('powerstat', backref='hourlystatistics')
    events = db.relationship('eventstat', backref='hourlystatistics')
    
    last_updated = db.Column(db.DateTime)

    def __init__(self, heat, power, events):
        self.heat = heat
        self.power = power
        self.events = events
        last_updated = datetime.now()

class DailyStatistics(db.Model):
    __tablename__ = 'dailystatistics'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('statistics.id'))

    node = db.relationship('NodeModel', backref='hourlystatistics')
    icpe = db.relationship('iCPEModel', backref='hourlystatistics')
    zwavedevice = db.relationship('ZWaveDeviceModel',
                                  backref='hourlystatistics')

    heat = db.relationship('heatstat', backref='hourlystatistics')
    power = db.relationship('powerstat', backref='hourlystatistics')
    events = db.relationship('eventstat', backref='hourlystatistics')
 

    last_updated = db.Column(db.DateTime)

    def __init__(self, heat, power, events):
        self.heat = heat
        self.power = power
        self.events = events
        last_updated = datetime.now()

class WeeklyStatistics(db.Model):
    __tablename__ = 'weeklystatistics'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('statistics.id'))
     
    node = db.relationship('NodeModel', backref='hourlystatistics')
    icpe = db.relationship('iCPEModel', backref='hourlystatistics')
    zwavedevice = db.relationship('ZWaveDeviceModel',
                                  backref='hourlystatistics')

    heat = db.relationship('heatstat', backref='hourlystatistics')
    power = db.relationship('powerstat', backref='hourlystatistics')
    events = db.relationship('eventstat', backref='hourlystatistics')
    
    last_updated = db.Column(db.DateTime)

    def __init__(self, heat, power, events):
        self.heat = heat
        self.power = power
        self.events = events
        self.last_updated = datetime.now()

'''
Statistics Model
'''

class HeatStatModel(db.Model):
    __tablename__ = 'heatstat'
    id = db.Column(db.Integer, primary_key=True)
    hourly_id = db.Column(db.Integer, db.ForeignKey('hourlystatistics.id'))
    daily_id = db.Column(db.Integer, db.ForeignKey('dailystatistics.id'))
    weekly_id = db.Column(db.Integer, db.ForeignKey('weeklystatistics.id'))

    high = db.Column(db.Float)
    low = db.Column(db.Float)
    average = db.Column(db.Float)

    def __init__(self):
        pass

class PowerStatModel(db.Model):
    __tablename__ = 'powerstat'
    id = db.Column(db.Integer, primary_key=True)
    hourly_id = db.Column(db.Integer, db.ForeignKey('hourlystatistics.id'))
    daily_id = db.Column(db.Integer, db.ForeignKey('dailystatistics.id'))
    weekly_id = db.Column(db.Integer, db.ForeignKey('weeklystatistics.id'))

    high = db.Column(db.Float)
    low = db.Column(db.Float)
    average = db.Column(db.Float)

    def __init__(self):
        pass

class EventStatModel(db.Model):
    __tablename__ = 'eventstat'
    id = db.Column(db.Integer, primary_key=True)
    hourly_id = db.Column(db.Integer, db.ForeignKey('hourlystatistics.id'))
    daily_id = db.Column(db.Integer, db.ForeignKey('dailystatistics.id'))
    weekly_id = db.Column(db.Integer, db.ForeignKey('weeklystatistics.id'))
  
    respond = db.Column(db.Integer)
    report = db.Column(db.Integer)
    command = db.Column(db.Integer)

    critcial = db.Column(db.Integer)
    normal = db.Column(db.Integer)

    def __init__(self):
        pass
