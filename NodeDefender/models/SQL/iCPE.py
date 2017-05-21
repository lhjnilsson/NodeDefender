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
    
    firmware = db.Column(db.String(12))
    hardware = db.Column(db.String(8))

    enabled =  db.Column(db.Boolean)
    created_on = db.Column(db.DateTime)
    last_online = db.Column(db.DateTime)
    sensors = db.relationship('SensorModel', backref='icpe',
                              cascade='save-update, merge, delete')
    notesticky = db.Column(db.String(150))
    heat = db.relationship('HeatModel', backref="icpe",
                           cascade="save-update, merge, delete")
    power = db.relationship('PowerModel', backref="icpe",
                           cascade="save-update, merge, delete")
    events = db.relationship('EventModel', backref="icpe",
                           cascade="save-update, merge, delete")

    messages = db.relationship('MessageModel', backref='icpe',
                               cascade='save-update, merge, delete')

    def __init__(self, macaddr):
        self.macaddr = macaddr.upper()
        self.enabled = False
        self.created_on = datetime.now()

    def __repr__(self):
        return '<Name %r, Mac %r>' % (self.name, self.macaddr)

    def to_json(self):
        if self.node:
            node = self.node.name
        else:
            node = 'Not assigned'

        icpe = {'name' : self.name,
                'macAddress' : self.macaddr,
                'ipaddr' : self.ipaddr,
                'createdAt' : str(self.created_on),
                'sensors' : str(len(self.sensors)),
                'mqttConnection' : self.mqtt[0].ipaddr,
                'node' : node,
                'online' : 'false'}
        return icpe

class SensorModel(db.Model):
    '''
    ZWave Sensor, child of iCPE
    '''
    __tablename__ = 'sensor'
    id = db.Column(db.Integer, primary_key=True)
    icpe_id = db.Column(db.Integer, db.ForeignKey('icpe.id'))
    
    name = db.Column(db.String(64))
    sensorid = db.Column(db.String(4))
    
    brand = db.Column(db.String(64))
    productname = db.Column(db.String(64))
    manufacturerid = db.Column(db.String(16))
    productid = db.Column(db.String(16))
    producttypeid = db.Column(db.String(16))
    librarytype = db.Column(db.String(64))
    devicetype = db.Column(db.String(64))
  
    commandclasses = db.relationship('CommandClassModel', backref='sensor',
                                cascade='save-update, merge, delete')
    heat = db.relationship('HeatModel', backref="sensor",
                           cascade="save-update, merge, delete")
    power = db.relationship('PowerModel', backref="sensor",
                           cascade="save-update, merge, delete")
    events = db.relationship('EventModel', backref="sensor",
                           cascade="save-update, merge, delete")

    messages = db.relationship('MessageModel', backref='sensor',
                               cascade='save-update, merge, delete')


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

class CommandClassModel(db.Model):
    __tablename__ = 'commandclass'
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'))
    number = db.Column(db.String(2))
    name = db.Column(db.String(20))
    types = db.relationship('CommandClassTypeModel', backref="commandclass",
                            cascade="save-update, merge, delete")
    supported = db.Column(db.Boolean)
    events = db.relationship('EventModel', backref="sensorcc",
                           cascade="save-update, merge, delete")

    def __init__(self, cc):
        self.ccc = cc[:2]
        self.supported = False

class CommandClassTypeModel(db.Model):
    __tablename__ = 'commandclasstype'
    id = db.Column(db.Integer, primary_key=True)
    commandclass_id = db.Column(db.Integer, db.ForeignKey('commandclass.id'))
    number = db.Column(db.String(2))
    name = db.Column(db.String(40))
    supported = db.Column(db.Boolean)

    def __init__(self, number):
        self.number = str(number)
        self.supported = False
