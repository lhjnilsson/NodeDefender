from ... import db
from datetime import datetime

class iCPEModel(db.Model):
    '''
    iCPE attached to a Node
    '''
    __tablename__ = 'icpe'
    id = db.Column(db.Integer, primary_key=True)
    node_id = db.Column(db.Integer, db.ForeignKey('node.id'))
    mac = db.Column(db.String(12), unique=True)
    online =  db.Column(db.Boolean)
    last_online = db.Column(db.DateTime)
    sensors = db.relationship('SensorModel', backref='icpe')
    notesticky = db.Column(db.String(150))

    def __init__(self, mac):
        self.mac = mac.upper()
        self.created_on = datetime.now()

    def __repr__(self):
        return '<Node %r, Mac %r>' % (self.alias, self.mac)


class SensorModel(db.Model):
    '''
    ZWave Sensor, child of iCPE
    '''
    __tablename__ = 'sensor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    icpe_id = db.Column(db.Integer, db.ForeignKey('icpe.id'))
    vid = db.Column(db.String(10))
    roletype = db.Column(db.String(10))
    devicetype = db.Column(db.String(10))
    pid = db.Column(db.String(10))
    generic_class = db.Column(db.String(10))
    productname = db.Column(db.String(30))
    brandname = db.Column(db.String(30))
    cmdclasses = db.relationship('SensorClassModel', backref='sensor')
    statistics = db.relationship('StatisticsModel', backref="sensor",
                                 uselist=False)

    def __init__(self, nodeid, vid, ptype, pid, generic_class, productname,
                 brandname):
        self.name = productname
        self.nodeid = nodeid
        self.vid = vid
        self.ptype = ptype
        self.pid = pid
        self.generic_class = generic_class
        self.productname = productname
        self.brandname = brandname

class SensorClassModel(db.Model):
    __tablename__ = 'sensorclass'
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'))
    cmdclass = db.Column(db.String(20))
    types = db.Column(db.String(200))

    def __init__(self, cmdclass, types):
        self.cmdclass = cmdclass
        if type(types) is list:
            types = str(types)[1:-1]
        self.types = types
