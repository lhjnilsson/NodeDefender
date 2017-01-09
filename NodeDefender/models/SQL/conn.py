from ... import db
from . import iCPEModel
from datetime import datetime

mqtt_icpe = db.Table('mqtt_icpe',
                     db.Column('mqtt_id', db.Integer, db.ForeignKey('mqtt.id')),
                     db.Column('icpe_id', db.Integer, db.ForeignKey('icpe.id')))


class MQTTModel(db.Model):
    __tablename__ = 'mqtt'
    id = db.Column(db.Integer, primary_key=True)
    ipaddr = db.Column(db.String(20))
    port = db.Column(db.Integer)
    username = db.Column(db.String(64))
    password = db.Column(db.String(64))

    icpes = db.relationship('iCPEModel', secondary=mqtt_icpe,
                            backref=db.backref('mqtt', lazy='dynamic'))

    created_at = db.Column(db.DateTime)

    def __init__(self, ipaddr, port, username = None, password = None):
        self.ipaddr = ipaddr
        self.port = int(port)
        self.username = username
        self.password = password
        self.created_at = datetime.now()
