from NodeDefender.db.sql import SQL
from datetime import datetime

class NodeModel(SQL.Model):
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
    id = SQL.Column(SQL.Integer, primary_key=True)
    name = SQL.Column(SQL.String(40), unique=True)
    location = SQL.relationship('LocationModel', uselist=False, backref='node')
    created_on = SQL.Column(SQL.DateTime)
    notes = SQL.relationship('NodeNotesModel', backref='node')
    notesticky = SQL.Column(SQL.String(150))
    icpe = SQL.relationship('iCPEModel', backref='node', uselist=False)
    heat = SQL.relationship('HeatModel', backref="node",
                           cascade="save-update, merge, delete")
    power = SQL.relationship('PowerModel', backref="node",
                           cascade="save-update, merge, delete")
    events = SQL.relationship('EventModel', backref="node",
                           cascade="save-update, merge, delete")
    messages = SQL.relationship('MessageModel', backref='node',
                               cascade='save-update, merge, delete')

    def __init__(self, name):
        self.name = name
        self.created_on = datetime.now()


    def to_json(self):
        return {'name' : self.name,
                'location' : {'latitude' : self.location.latitude,
                              'longitude' : self.location.longitude
                             }
               }

class LocationModel(SQL.Model):
    '''
    One-to-one Table representing Location for iCPE
    '''
    __tablename__ = 'location'
    id = SQL.Column(SQL.Integer, primary_key=True)
    node_id = SQL.Column(SQL.Integer, SQL.ForeignKey('node.id'))
    group_id = SQL.Column(SQL.Integer, SQL.ForeignKey('group.id'))
    street = SQL.Column(SQL.String(30))
    city = SQL.Column(SQL.String(30))
    latitude = SQL.Column(SQL.String(10))
    longitude = SQL.Column(SQL.String(10))
    
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

class NodeNotesModel(SQL.Model):
    __tablename__ = 'nodenotes'

    id = SQL.Column(SQL.Integer, primary_key=True)
    node_id = SQL.Column(SQL.Integer, SQL.ForeignKey('node.id'))
    author = SQL.Column(SQL.String(80))
    note = SQL.Column(SQL.String(150))
    created_on = SQL.Column(SQL.DateTime)

    def __init__(self, author, note):
        self.author = author
        self.note = note
        self.created_on = datetime.now()
