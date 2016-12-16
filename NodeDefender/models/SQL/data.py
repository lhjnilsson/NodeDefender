class Statistics(db.Model):
    __tablename__ = 'statistics'
    id = db.Column(db.Integer, primary_key=True)
    
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    group = db.relationship('GroupModel', backref='statistics')

    hourly = db.relationship('HourlyStatistics', backref="statistics")
    daily = db.relationship('DailyStatistics', backref='statistics')
    weekly = db.relationship('WeeklyStatistics', backref='statistics')
    
    node = db.relationship('NodeStatistics', backref='statistics')
    icpe = db.relationship('iCPEStatistics', backref='statistics')
    ZWaveDevice = db.relationship('ZWaveDeviceStatistics', backref='statistics')

    def __init__(self):
        pass

class NodeStatistics(db.Model):
    __tablename__ = 'nodestatistics'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('statistics.id'))
    
    node = db.relationship('NodeModel', backref='nodestatistics')

    hourly = db.relationship('HourlyStatistics', backref='nodestatistics')
    daily = db.relationship('DailyStatistics', backref='nodestatistics')
    weekly = db.relationship('WeeklyStatistics', backref='nodestatistics')

    def __init__(self):
        pass

class iCPEStatistics(db.Model):
    __tablename__ = 'icpestatistics'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('statistics.id'))

    node = db.relationship('NodeModel', backref='nodestatistics')
    icpe = db.relationship('iCPEModel', backref='icpestatisctics')

    hourly = db.relationship('HourlyStatistics', backref='icpestatistics')
    daily = db.relationship('DailyStatistics', backref='icpestatistics')
    weekly = db.relationship('WeeklyStatistics', backref='icpestatistics')

    def __init__(self):
        pass

class ZWaveDeviceStatistics(db.Model):
    __tablename__ = 'zwavedevicestatistics'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('statistics.id'))
    
    node = db.relationship('NodeModel', backref='nodestatistics')
    icpe = db.relationship('iCPEModel', backref='icpestatisctics')
    zwavedevice = db.relationship('ZWaveDeviceModel',
                                  backref='zwavedevicestatistics')

    hourly = db.relationship('HourlyStatistics',
                             backref='zwavedevicestatistics')
    daily = db.relationship('DailyStatistics', backref='zwavedevicestatistics')
    weekly = db.relationship('WeeklyStatistics', backref='zwavedevicestatistics')

    def __init__(self):
        pass

'''
Hourly, Daily and Weekly container of Heat, Power and Events.


'''

GroupTags = db.Table('GroupTags',
                     db.Column('NodestatisticsID', db.Integer,
                               db.ForeignKey('NodeStatistics.id')),
                     db.Column(

class HourlyStatistics(db.Model):
    __tablename__ = 'hourlystatistics'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('statistics.id'))
    
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
    parent_id = db.Column(db.Integer, db.ForeginKey('statistics.id'))
    
    last_updated = db.Column(db.DateTime)

    def __init__(self, heat, power, events):
        self.heat = heat
        self.power = power
        self.events = events
        last_updated = datetime.now()

class WeeklyStatistics(db.Model):
    __tablename__ = 'weeklystatistics'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeginKey('statistics.id'))
    
    last_updated = db.Column(db.DateTime)

    def __init__(self, heat, power, events):
        self.heat = heat
        self.power = power
        self.events = events
        self.last_updated = datetime.now()

### NOde specific models

class GroupHeatModel(db.Model):
    __tablename__ = 'groupheat'
    id = db.Column(db.Integer, primary_key=True)
    group = db.relationship('GroupModel', backref='groupheat')
    date = db.Column(db.DateTime)

    high = db.Column(db.Float)
    low = db.Column(db.Float)
    average = db.Column(db.Float)

    nodeheat = db.relationsihp('NodeHeatModel', backref='groupheat')

    def __init__(self):
        pass

class NodeHeatModel(db.Model):
    __tablename__ = 'nodeheat'
    id = db.Column(db.Integer, primary_key=True)
    node = db.relationship('NodeModel', backref='nodeheat')
    date = db.Column(db.DateTime)

    high = db.Column(db.Float)
    low = db.Column(db.Float)
    average = db.Column(db.Float)

    zwaveheat = db.relationsihp('ZWaveHeatModel', backref='nodeheat')

    def __init__(self):
        pass

class ZWaveHeatModel(db.Model):
    __tablename__ = 'zwaveheat'
    id = db.Column(db.Integer, primary_key=True)
    zwavedevice = db.relationship('ZWaveDeviceModel', backref='zwaveheat')
    date = db.Column(db.DateTime)

    high = db.Column(db.Float)
    low = db.Column(db.Float)
    average = db.Column(db.Float)

    def __init__(self):
        pass

class GroupPowerModel(db.Model):
    __tablename__ = 'grouppower'
    id = db.Column(db.Integer, primary_key=True)
    group = db.relationship('GroupModel', backref='grouppower')
    date = db.Column(db.DateTime)

    high = db.Column(db.Float)
    low = db.Column(db.Float)
    average = db.Column(db.Float)

    nodeheat = db.relationsihp('NodePowerModel', backref='grouppower')

    def __init__(self):
        pass

class NodePowerModel(db.Model):
    __tablename__ = 'nodepower'
    id = db.Column(db.Integer, primary_key=True)
    node = db.relationship('NodeModel', backref='nodepower')
    date = db.Column(db.DateTime)

    high = db.Column(db.Float)
    low = db.Column(db.Float)
    average = db.Column(db.Float)

    zwaveheat = db.relationsihp('ZWavePowerModel', backref='nodepower')

    def __init__(self):
        pass

class ZWavePowerModel(db.Model):
    __tablename__ = 'zwavepower'
    id = db.Column(db.Integer, primary_key=True)
    zwavedevice = db.relationship('ZWaveDeviceModel', backref='zwavepower')
    date = db.Column(db.DateTime)

    high = db.Column(db.Float)
    low = db.Column(db.Float)
    average = db.Column(db.Float)

    def __init__(self):
        pass


## old
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

