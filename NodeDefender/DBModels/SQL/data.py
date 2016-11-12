'''

No idea why i cant have Major holder of all the Statitstics- tables...
somethings to work on later..

class Statistics(db.Model):
    __tablename__ = 'statistics'
    id = db.Column(db.Integer, primary_key=True)
    keyID = db.Column(db.Integer)
    hourly = db.relationship('HourlyStatistics', uselist=False,
                             backref="statistics")
    daily = db.relationship('DailyStatistics', uselist=False,
                            backref='statistics')
    weekly = db.relationship('WeeklyStatistics', uselist=False,
                             backref='statistics')
    dailylog = db.relationship('DailylogStatistics', backref='statistics')
    weeklylog = db.relationship('WeeklylogStatistics', backref='statistics')

    def __init__(self, keyID):
        self.keyID = keyID
'''
class HourlyStatistics(db.Model):
    __tablename__ = 'hourlystatistics'
    id = db.Column(db.Integer, primary_key=True)
    #parent_id = db.Column(db.Integer, db.ForeignKey('statistics.id'))
    heat = db.Column(db.Float)
    power = db.Column(db.Float)
    events = db.Column(db.Integer)
    last_updated = db.Column(db.DateTime)

    def __init__(self, heat, power, events):
        self.heat = heat
        self.power = power
        self.events = events
        last_updated = datetime.now()

class DailyStatistics(db.Model):
    __tablename__ = 'dailystatistics'
    id = db.Column(db.Integer, primary_key=True)
    #parent_id = db.Column(db.Integer, db.ForeginKey('statistics.id'))
    heat = db.Column(db.Float)
    power = db.Column(db.Float)
    events = db.Column(db.Integer)
    last_updated = db.Column(db.DateTime)

    def __init__(self, heat, power, events):
        self.heat = heat
        self.power = power
        self.events = events
        last_updated = datetime.now()

class WeeklyStatistics(db.Model):
    __tablename__ = 'weeklystatistics'
    id = db.Column(db.Integer, primary_key=True)
    #parent_id = db.Column(db.Integer, db.ForeginKey('statistics.id'))
    heat = db.Column(db.Float)
    power = db.Column(db.Float)
    events = db.Column(db.Integer)
    last_updated = db.Column(db.DateTime)

    def __init__(self, heat, power, events):
        self.heat = heat
        self.power = power
        self.events = events
        self.last_updated = datetime.now()

class HourlylogStatistics(db.Model):
    __tablename__ = 'hourlylogstatistics'
    id = db.Column(db.Integer, primary_key=True)
    heat = db.Column(db.Float)
    power = db.Column(db.Float)
    events = db.Column(db.Integer)
    last_updated = db.Column(db.DateTime)

    def __init__(self, heat, power, events):
        self.heat = heat
        self.power = power
        self.events = events
        self.last_updated = datetime.now()


class DailylogStatistics(db.Model):
    __tablename__ = 'dailylogstatistics'
    id = db.Column(db.Integer, primary_key=True)
    #parent_id = db.Column(db.Integer, db.ForeginKey('statistics.id'))
    heat = db.Column(db.Float)
    power = db.Column(db.Float)
    events = db.Column(db.Integer)
    last_updated = db.Column(db.DateTime)

    def __init__(self, heat, power, events):
        self.heat = heat
        self.power = power
        self.events = events
        self.last_updated = datetime.now()

class WeeklylogStatistics(db.Model):
    __tablename__ = 'weeklylogstatistics'
    id = db.Column(db.Integer, primary_key=True)
    #parent_id = db.Column(db.Integer, db.ForeginKey('statistics.id'))
    heat = db.Column(db.Float)
    power = db.Column(db.Float)
    events = db.Column(db.Integer)
    last_updated = db.Column(db.DateTime)

    def __init__(self, heat, power, events):
        self.heat = heat
        self.power = power
        self.events = events
        self.last_updated = datetime.now()


### NOde specific models

class NodeHeatStatModel(db.Model):
    __tablename__ = 'nodeheatstat'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('icpe.id'))
    parent = db.relationship('iCPEModel', backref='Heats')
    nodeid = db.Column(db.Integer)
    events = db.Column(db.Integer)
    heat = db.Column(db.Float)
    date = db.Column(db.DateTime)

    def __init__(self, nodeid, events, heat, date):
        self.nodeid = int(nodeid)
        self.events = int(events)
        self.heat = float(heat)
        self.date = date

class NodePowerStatModel(db.Model):
    __tablename__ = 'nodepowerstat'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('icpe.id'))
    parent = db.relationship('iCPEModel', backref='Powers')
    nodeid = db.Column(db.Integer)
    events = db.Column(db.Integer)
    power = db.Column(db.Float)
    date = db.Column(db.DateTime)

    def __init__(self, nodeid, events, power, date):
        self.nodeid = int(nodeid)
        self.events = int(events)
        self.power = float(power)
        self.date = date

class NodeEventModel(db.Model):
    '''
    ZWave event, child of iCPE
    '''
    __tablename__ = 'nodeevent'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('icpe.id'))
    parent = db.relationship('iCPEModel', backref='nodeevent')
    nodeid = db.Column(db.Integer)
    productname = db.Column(db.String(30))
    fonticon = db.Column(db.String(8))
    created_on = db.Column(db.DateTime)

    def __init__(self, nodeid, productname, fonticon):
        self.nodeid = int(nodeid)
        self.productname = productname
        self.fonticon = fonticon
        self.created_on = datetime.now()

class NodeHeatModel(db.Model):
    __tablename__ = 'nodeheat'
    '''
    Node Heat, child of iCPE
    '''
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('icpe.id'))
    parent = db.relationship('iCPEModel', backref='nodeheat')
    nodeid = db.Column(db.Integer)
    heat = db.Column(db.Float)
    unit = db.Column(db.String(10))
    fonticon = db.Column(db.String(8))
    created_on = db.Column(db.DateTime)

    def __init__(self, nodeid, heat, unit, fonticon):
        self.nodeid = int(nodeid)
        self.heat = heat
        self.unit = unit
        self.fonticon = fonticon
        self.created_on = datetime.now()

class NodePowerModel(db.Model):
    __tablename__ = 'nodepower'
    '''
    Node Power, child of iCPE
    '''
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('icpe.id'))
    parent = db.relationship('iCPEModel', backref='nodepower')
    nodeid = db.Column(db.Integer)
    power = db.Column(db.Float)
    unit = db.Column(db.String(10))
    fonticon = db.Column(db.String(8))
    created_on = db.Column(db.DateTime)

    def __init__(self, nodeid, power, unit, fonticon):
        self.nodeid = int(nodeid)
        self.power = power
        self.unit = unit
        self.fonticon = fonticon
        self.created_on = datetime.now()


