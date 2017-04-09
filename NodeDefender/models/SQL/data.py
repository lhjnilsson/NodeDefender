from ... import db
from datetime import datetime

class HeatModel(db.Model):
    __tablename__ = 'heat'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)

    node_id = db.Column(db.Integer, db.ForeignKey('node.id'))
    icpe_id = db.Column(db.Integer, db.ForeignKey('icpe.id'))
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'))
    
    high = db.Column(db.Float)
    low = db.Column(db.Float)
    average = db.Column(db.Float)

    def __init__(self, heat):
        self.high = heat
        self.low = heat
        self.average = heat
        self.date = date

class PowerModel(db.Model):
    __tablename__ = 'power'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)

    node_id = db.Column(db.Integer, db.ForeignKey('node.id'))
    icpe_id = db.Column(db.Integer, db.ForeignKey('icpe.id'))
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'))

    high = db.Column(db.Float)
    low = db.Column(db.Float)
    average = db.Column(db.Float)
    total = db.Column(db.Float)

    def __init__(self, power = 0.0, date = datetime.now()):
        self.high = power
        self.low = power
        self.average = power
        self.total = power
        self.date = date

class EventModel(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)

    node_id = db.Column(db.Integer, db.ForeignKey('node.id'))
    icpe_id = db.Column(db.Integer, db.ForeignKey('icpe.id'))
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'))
    cmdclass_id = db.Column(db.Integer, db.ForeignKey('sensorclass.id'))
    classtype = db.Column(db.String(8))
    value = db.Column(db.String(8))

    critcial = db.Column(db.Boolean)
    normal = db.Column(db.Boolean)

    def __init__(self, classtype, value, date = None):
        self.classtype = classtype
        self.value = value
        self.date = date if date else datetime.now()
