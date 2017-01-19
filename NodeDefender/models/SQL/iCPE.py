from ... import db
from datetime import datetime

class iCPEModel(db.Model):
    '''
    iCPE attached to a Node
    '''
    __tablename__ = 'icpe'
    id = db.Column(db.Integer, primary_key=True)
    node_id = db.Column(db.Integer, db.ForeignKey('node.id'))
    name = db.Column(db.String(64))
    mac = db.Column(db.String(12), unique=True)
    ipaddr = db.Column(db.String(32))
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
    icpe_id = db.Column(db.Integer, db.ForeignKey('icpe.id'))
    
    name = db.Column(db.String(32))
    sensorid = db.Column(db.Integer)
    
    vendorid = db.Column(db.String(16))
    productid = db.Column(db.String(16))
    brandname = db.Column(db.String(32))
    productname = db.Column(db.String(32))
       
    roletype = db.Column(db.String(32))
    devicetype = db.Column(db.String(32))
    generic_class = db.Column(db.String(16))
   
    cmdclasses = db.relationship('SensorClassModel', backref='sensor')

    def __init__(self, sensorid):
        self.sensorid = int(sensorid)

        self.name = "None"

class SensorClassModel(db.Model):
    __tablename__ = 'sensorclass'
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'))
    cmdclass = db.Column(db.String(20))
    classtypes = db.Column(db.String(200))

    def __init__(self, cmdclass, types):
        self.cmdclass = cmdclass
        if type(types) is list:
            types = str(types)[1:-1]
        self.types = types
