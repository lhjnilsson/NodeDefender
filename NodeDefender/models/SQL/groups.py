from ... import db

class GroupModel(db.Model):
    '''
    Representing one group containing iCPEs and Users
    '''
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    created_on = db.Column(db.DateTime)
   
    messages = db.relationship('GroupMessageModel', backref='groupmessages')
    
    nodes = db.relationship('NodeModel', backref='groupnodes')
    statistics = db.relationship('StatisticsModel', backref='groupstatistics')
    def __init__(self, name):
        self.name = name
        self.created_on = datetime.now()

class GroupMessageModel(db.Model):
    '''
    Common messages for a group
    '''
    __tablename__ = 'groupmessage'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    created_on = db.Column(db.DateTime)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('UserModel', backref='groupmessageauthor')
    subject = db.Column(db.String(50))
    message = db.Column(db.String(300))

    def __init__(self, author, subject, message):
        self.author = author
        self.message = message
