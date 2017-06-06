from ... import db
from datetime import datetime
from .nodes import LocationModel

class MessageModel(db.Model):
    '''
    Representing one group containing iCPEs and Users
    '''
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    subject = db.Column(db.String(50))
    body = db.Column(db.String(180))
    
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    node_id = db.Column(db.Integer, db.ForeignKey('node.id'))
    icpe_id = db.Column(db.Integer, db.ForeignKey('icpe.id'))
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'))


    def __init__(self, subject, body):
        self.subject = subject
        self.body = body
        self.date = datetime.now()

    def to_json(self):
        if self.group:
            group = self.group.name
        else:
            group = False
        
        if self.user:
            user = self.user.name
        else:
            user = False

        if self.node:
            node = self.node.name
        else:
            node = False

        if self.icpe:
            icpe = self.icpe.name
        else:
            icpe = False

        if self.sensor:
            sensor = self.sensor.name
        else:
            sensor = False

        return {'group' : group, 'user' : user,\
                'node' : node, 'icpe' : icpe, 'sensor' : sensor,\
                'subject' : self.subject,
                'body' : self.body,
                'date' : str(self.date)}
