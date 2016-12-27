from ... import db

class MQTTModel(db.Model):
    __tablename__ = 'mqtt'
    id = db.Column(db.Integer, primary_key=True)
    ipaddr = db.Column(db.String(20))
    port = db.Column(db.String(10))
    username = db.Column(db.String(10))
    password = db.Column(db.String(10))

    created_at = db.Column(db.DateTime)

    def __init__(self, ipaddr, port, username = None, password = None):
        self.ipaddr = ipaddr
        self.port = port
        self.username = username
        self.password = password
