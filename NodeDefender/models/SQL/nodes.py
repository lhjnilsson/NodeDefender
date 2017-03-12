from ... import db
from datetime import datetime

class NodeModel(db.Model):
    '''
    Nodes represent a place that can contain one or more iCPEs

    Parent is the GroupModel that owns the Node
    Alias is the Name of the Node
    Location is stored in one-to-one Relation(LocationModel)
    Notes is to enter notebook for the Node
    NoteSticky is a sticky note for that node

    iCPES is relationship to List of iCPEs in that Node
    '''
    __tablename__ = 'node'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    name = db.Column(db.String(40), unique=True)
    location = db.relationship('LocationModel', uselist=False, backref='node')
    created_on = db.Column(db.DateTime)
    statistics = db.relationship('StatisticsModel', backref='node', uselist=False)
    notes = db.relationship('NodeNotesModel', backref='node')
    notesticky = db.Column(db.String(150))
    icpe = db.relationship('iCPEModel', backref='node', uselist=False)

    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.created_on = datetime.now()


    def to_json(self):
        return {'name' : self.name,
                'location' : {'latitude' : self.location.latitude,
                              'longitude' : self.location.longitude
                             }
               }

class LocationModel(db.Model):
    '''
    One-to-one Table representing Location for iCPE
    '''
    __tablename__ = 'location'
    id = db.Column(db.Integer, primary_key=True)
    node_id = db.Column(db.Integer, db.ForeignKey('node.id'))
    street = db.Column(db.String(30))
    city = db.Column(db.String(30))
    latitude = db.Column(db.String(10))
    longitude = db.Column(db.String(10))
    
    def __init__(self, street, city, latitude, longitude):
        self.street = street
        self.city = city
        self.latitude = latitude
        self.longitude = longitude

    def to_json(self):
        return {'street' : self.street, 'city' : self.city,
                'latitude' : self.latitude, 'longitude' : self.longitude}

    def __repr__(self):
        return '<%r, %r>' % (self.street, self.city)

class NodeNotesModel(db.Model):
    __tablename__ = 'nodenotes'

    id = db.Column(db.Integer, primary_key=True)
    node_id = db.Column(db.Integer, db.ForeignKey('node.id'))
    author = db.Column(db.String(80))
    note = db.Column(db.String(150))
    created_on = db.Column(db.DateTime)

    def __init__(self, author, note):
        self.author = author
        self.note = note
        self.created_on = datetime.now()
