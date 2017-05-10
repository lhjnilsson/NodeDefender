from ... import db
from datetime import datetime
from .nodes import LocationModel
i
class MessageModel(db.Model):
    '''
    Representing one group containing iCPEs and Users
    '''
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    subject = db.Column(db.String(50))
    body = db.Column(db.String(350))
    
    def __init__(self, subject, body):
        self.subject = subject
        self.body = body
        self.date = datetime.now()

    def to_json(self):
        if self.group:
            group : self.group.name
        
        if self.user:
            user : self.user.name

        if self.node:
            node : self.node.name

        if self.icpe:
            icpe : self.icpe.name

        if self.sensor:
            sensor : self.sensor.name

        return {'name' : self.name, 'email' : self.email, 'date' :
                str(self.date), 'group' : group}
