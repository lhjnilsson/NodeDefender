from ... import db

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

    def __init__(self):
        pass

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

    def __init__(self):
        pass

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

    def __init__(self):
        pass
