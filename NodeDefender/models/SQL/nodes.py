class NodeModel(db.Model):
    '''
    Nodes represent a place that can contain one or more iCPEs
    '''
    __tablename__ = 'node'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    parent = db.relationship('GroupModel', bakref='node')
    
    alias = db.Column(db.String(20))
    location = db.relationship('LocationModel', uselist=False, backref='node')
    created_on = db.Column(db.DateTime)

    notes = db.relationship('NodeNotesModel', backref='node')
    notesticky = db.Column(db.String(150))

    iCPE = db.relationship('iCPEModel', backref='node')

    def __init__(self):
        pass

class LocationModel(db.Model):
    '''
    One-to-one Table representing Location for iCPE
    '''
    __tablename__ = 'location'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('icpe.id'))
    street = db.Column(db.String(30))
    city = db.Column(db.String(30))
    geolat = db.Column(db.String(10))
    geolong = db.Column(db.String(10))
    
    def __init__(self, street, city):
        self.street = street
        self.city = city
        geo = Nominatim()
        location = geo.geocode(city + ' ' + street, timeout = 10)
        if not location: # If city and street is not recognized
            location = geo.geocode('Gothenburg') # change this later...
        self.geolat = location.latitude
        self.geolong = location.longitude

    def __repr__(self):
        return '<Alias %r. %r, %r>' % (self.alias, self.street, self.city)

class NodeNotesModel(db.Model):
    __tablename__ = 'nodenotes'

    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('icpe.id'))
    parent = db.relationship('iCPEModel', backref='nodenotes')
    author = db.Column(db.String(80))
    note = db.Column(db.String(150))
    created_on = db.Column(db.DateTime)

    def __init__(self, author, note):
        self.author = author
        self.note = note
        self.created_on = datetime.now()
