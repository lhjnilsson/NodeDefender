from ... import db
from .nodes import icpe_list

class iCPEModel(db.Model):
    '''
    iCPE attached to a Node
    '''
    __tablename__ = 'icpe'
    id = db.Column(db.Integer, primary_key=True)
    nodes = db.relationship('NodeModel', secondary=icpe_list,
                           backref=db.backref('icpe', lazy='dynamic'))
    
    mac = db.Column(db.String(12), unique=True)
    alias = db.Column(db.String(20), unique=True)
    created_on = db.Column(db.DateTime)
    online =  db.Column(db.Boolean)
    last_online = db.Column(db.DateTime)
    znodes = db.relationship('NodeModel', backref='icpeznodes')
    notesticky = db.Column(db.String(150))

    hourlystatistics = db.relationship('HourlyStatisticsModel', backref='icpehourly')
    dailystatistics = db.relationship('DailyStatisticsModel', backref='icpedaily')
    weeklystatistics = db.relationship('WeeklyStatisticsModel', backref='icpeweekly')


    def __init__(self, mac, alias):
        self.mac = mac.upper()
        self.alias = alias.capitalize()
        self.created_on = datetime.now()
        logger.info('iCPE {} succesfully added'.format(self.mac))

    def __repr__(self):
        return '<Node %r, Mac %r>' % (self.alias, self.mac)


class ZWaveDeviceModel(db.Model):
    '''
    ZWave Node, child of iCPE
    '''
    # Table storing Zwave nodes on iCPE Nodes
    __tablename__ = 'zwavedevice'
    id = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(20))
    parent_id = db.Column(db.Integer, db.ForeignKey('icpe.id'))
    nodeid = db.Column(db.Integer)
    vid = db.Column(db.String(10))
    roletype = db.Column(db.String(10))
    devicetype = db.Column(db.String(10))
    pid = db.Column(db.String(10))
    generic_class = db.Column(db.String(10))
    productname = db.Column(db.String(30))
    brandname = db.Column(db.String(30))
    zwaveclasses = db.relationship('ZWaveClassModel', backref='zwavedeviceclasses')

    hourlystatistics = db.relationship('HourlyStatisticsModel',
                                       backref='zwavedevicehourly')
    dailystatistics = db.relationship('DailyStatisticsModel',
                                      backref='zwavedevicedaily')
    weeklystatistics = db.relationship('WeeklyStatisticsModel',
                                       backref='zwavedeviceweekly')


    def __init__(self, nodeid, vid, ptype, pid, generic_class, productname,
                 brandname):
        self.alias = productname
        self.nodeid = nodeid
        self.vid = vid
        self.ptype = ptype
        self.pid = pid
        self.generic_class = generic_class
        self.productname = productname
        self.brandname = brandname

class ZWaveClassModel(db.Model):
    __tablename__ = 'zwaveclass'
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('zwavedevice.id'))
    commandclass = db.Column(db.String(10))
    types = db.relationship('ZWaveClassTypeModel', backref='zwaveclasstype')

    def __init__(self, commandclass):
        self.commandclass = commandclass

class ZWaveClassTypeModel(db.Model):
    __tablename__ = 'zwaveclasstype'
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('zwaveclass.id'))
    classtype = db.Column(db.String(8))

    def __init__(self, classtype):
        self.classtype = classtype

