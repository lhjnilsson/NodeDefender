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
    macaddr = db.Column(db.String(12), unique=True)
    ipaddr = db.Column(db.String(32))
    enabled =  db.Column(db.Boolean)
    created_on = db.Column(db.DateTime)
    last_online = db.Column(db.DateTime)
    sensors = db.relationship('SensorModel', backref='icpe',
                              cascade='save-update, merge, delete')
    notesticky = db.Column(db.String(150))
    fields = db.relationship('FieldModel', backref='icpe',
                                cascade='save-update, merge, delete')
    heat = db.relationship('HeatModel', backref="icpe",
                           cascade="save-update, merge, delete")
    power = db.relationship('PowerModel', backref="icpe",
                           cascade="save-update, merge, delete")
    events = db.relationship('EventModel', backref="icpe",
                           cascade="save-update, merge, delete")

    def __init__(self, macaddr):
        self.macaddr = macaddr.upper()
        self.enabled = False
        self.created_on = datetime.now()

    def __repr__(self):
        return '<Name %r, Mac %r>' % (self.name, self.macaddr)

    def to_json(self):
        icpe = {'name' : self.name,
                'macAddress' : self.macaddr,
                'ipaddr' : self.ipaddr,
                'createdAt' : str(self.created_on),
                'sensors' : str(len(self.sensors)),
                'mqttConnection' : self.mqtt[0].ipaddr,
                'node' : self.node.name,
                'online' : 'false'}
        return icpe

class FieldModel(db.Model):
    __tablename__ = 'field'
    id = db.Column(db.Integer, primary_key=True)
    
    icpe_id = db.Column(db.Integer, db.ForeignKey('icpe.id'))
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'))
    cmdclass_id = db.Column(db.Integer, db.ForeignKey('sensorclass.id'))

    name = db.Column(db.String(16))
    display = db.Column(db.Boolean)
    type = db.Column(db.String(16))
    readonly = db.Column(db.Boolean)

    def __init__(self, name, type, readonly):
        self.name = str(name)
        self.display = True
        self.type = str(type)
        self.readonly = bool(readonly)

class SensorModel(db.Model):
    '''
    ZWave Sensor, child of iCPE
    '''
    __tablename__ = 'sensor'
    id = db.Column(db.Integer, primary_key=True)
    icpe_id = db.Column(db.Integer, db.ForeignKey('icpe.id'))
    
    name = db.Column(db.String(32))
    sensorid = db.Column(db.String(4))
    
    brand = db.Column(db.String(32))
    productname = db.Column(db.String(32))
    manufacturerid = db.Column(db.String(16))
    productid = db.Column(db.String(16))
    producttypeid = db.Column(db.String(16))
    librarytype = db.Column(db.String(32))
    devicetype = db.Column(db.String(32))
  
    cmdclasses = db.relationship('SensorClassModel', backref='sensor',
                                cascade='save-update, merge, delete')
    fields = db.relationship('FieldModel', backref='sensor',
                                cascade='save-update, merge, delete')
    heat = db.relationship('HeatModel', backref="sensor",
                           cascade="save-update, merge, delete")
    power = db.relationship('PowerModel', backref="sensor",
                           cascade="save-update, merge, delete")
    events = db.relationship('EventModel', backref="sensor",
                           cascade="save-update, merge, delete")


    def __init__(self, sensorid, sensorinfo):
        self.sensorid = str(sensorid)
        if sensorinfo:
            for key, value in sensorinfo.items():
                print(key.lower(), value)
                setattr(self, key.lower(), value)

            self.productname = self.name
    
    def to_json(self):
        return {'name' : self.name, 'sensorId' : self.sensorid,\
                'icpe' : self.icpe.macaddr,\
                'brand' : self.brand, 'productName' : str(self.productname)}

class SensorClassModel(db.Model):
    __tablename__ = 'sensorclass'
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'))
    classnumber = db.Column(db.String(2))
    classname = db.Column(db.String(20))
    classtypes = db.Column(db.String(200))
    fields = db.relationship('FieldModel', backref='sensorclass',
                                cascade='save-update, merge, delete')
    events = db.relationship('EventModel', backref="sensorclass",
                           cascade="save-update, merge, delete")

    def __init__(self, classnumber):
        self.classnumber = classnumber[:2]
