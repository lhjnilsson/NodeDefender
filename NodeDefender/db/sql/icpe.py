from NodeDefender.db.sql import SQL
from datetime import datetime

class iCPEModel(SQL.Model):
    '''
    iCPE attached to a Node
    '''
    __tablename__ = 'icpe'
    id = SQL.Column(SQL.Integer, primary_key=True)
    node_id = SQL.Column(SQL.Integer, SQL.ForeignKey('node.id'))
    name = SQL.Column(SQL.String(64))

    macaddr = SQL.Column(SQL.String(12), unique=True)
    ipaddr = SQL.Column(SQL.String(32))
    
    firmware = SQL.Column(SQL.String(12))
    hardware = SQL.Column(SQL.String(8))

    enabled =  SQL.Column(SQL.Boolean)
    created_on = SQL.Column(SQL.DateTime)
    last_online = SQL.Column(SQL.DateTime)
    sensors = SQL.relationship('SensorModel', backref='icpe',
                              cascade='save-update, merge, delete')
    notesticky = SQL.Column(SQL.String(150))
    heat = SQL.relationship('HeatModel', backref="icpe",
                           cascade="save-update, merge, delete")
    power = SQL.relationship('PowerModel', backref="icpe",
                           cascade="save-update, merge, delete")
    events = SQL.relationship('EventModel', backref="icpe",
                           cascade="save-update, merge, delete")

    messages = SQL.relationship('MessageModel', backref='icpe',
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
                'mqttConnection' : self.mqtt[0].host,
                'node' : node,
                'online' : 'false'}
        return icpe

class SensorModel(SQL.Model):
    '''
    ZWave Sensor, child of iCPE
    '''
    __tablename__ = 'sensor'
    id = SQL.Column(SQL.Integer, primary_key=True)
    icpe_id = SQL.Column(SQL.Integer, SQL.ForeignKey('icpe.id'))
    
    name = SQL.Column(SQL.String(64))
    sensorid = SQL.Column(SQL.String(4))

    vendor_id = SQL.Column(SQL.String(16))
    product_type = SQL.Column(SQL.String(16))
    product_id = SQL.Column(SQL.String(16))
    vendor_name = SQL.Column(SQL.String(64))
    product_name = SQL.Column(SQL.String(64))

    generic_class = SQL.Column(SQL.String(32))
    specific_class = SQL.Column(SQL.String(32))

    sleepable = SQL.Column(SQL.Boolean)
    wakeup_interval = SQL.Column(SQL.Integer)

    commandclasses = SQL.relationship('CommandClassModel', backref='sensor',
                                cascade='save-update, merge, delete')
    heat = SQL.relationship('HeatModel', backref="sensor",
                           cascade="save-update, merge, delete")
    power = SQL.relationship('PowerModel', backref="sensor",
                           cascade="save-update, merge, delete")
    events = SQL.relationship('EventModel', backref="sensor",
                           cascade="save-update, merge, delete")

    messages = SQL.relationship('MessageModel', backref='sensor',
                               cascade='save-update, merge, delete')


    def __init__(self, sensorid, sensorinfo = None):
        self.sensorid = str(sensorid)
        if sensorinfo:
            for key, value in sensorinfo.items():
                print(key.lower(), value)
                setattr(self, key.lower(), value)

            self.productname = self.name

    def columns(self):
        return ['sensorid', 'vendor_id', 'product_type', 'product_id',
                'generic_class', 'specific_class', 'sleepable',
                'wakeup_interval']

    def to_json(self):
        return {'name' : self.name, 'sensorId' : self.sensorid,\
                'icpe' : self.icpe.macaddr,\
                'brand' : self.brand, 'productName' : str(self.productname)}

class CommandClassModel(SQL.Model):
    __tablename__ = 'commandclass'
    id = SQL.Column(SQL.Integer, primary_key=True)
    sensor_id = SQL.Column(SQL.Integer, SQL.ForeignKey('sensor.id'))
    number = SQL.Column(SQL.String(2))
    name = SQL.Column(SQL.String(20))
    types = SQL.relationship('CommandClassTypeModel', backref="commandclass",
                            cascade="save-update, merge, delete")
    supported = SQL.Column(SQL.Boolean)
    web_field = SQL.Column(SQL.Boolean)
    events = SQL.relationship('EventModel', backref="commandclass",
                           cascade="save-update, merge, delete")

    def __init__(self, number, name):
        self.number = str(number)[:2]
        self.name = name
        self.supported = False

    def to_json(self):
        return {'name' : self.name, 'number' : self.number, 'webField' :
                self.web_field, 'supported' : self.supported, 'sensor' :
                self.sensor.sensorid, 'icpe' : self.sensor.icpe.macaddr}

    def columns(self):
        return ['number', 'name']

class CommandClassTypeModel(SQL.Model):
    __tablename__ = 'commandclasstype'
    id = SQL.Column(SQL.Integer, primary_key=True)
    commandclass_id = SQL.Column(SQL.Integer, SQL.ForeignKey('commandclass.id'))
    number = SQL.Column(SQL.String(2))
    name = SQL.Column(SQL.String(40))
    supported = SQL.Column(SQL.Boolean)
    web_field = SQL.Column(SQL.Boolean)
    events = SQL.relationship('EventModel', backref="commandclasstype",
                           cascade="save-update, merge, delete")

    def __init__(self, number):
        self.number = str(number)[:2]
        self.supported = False
