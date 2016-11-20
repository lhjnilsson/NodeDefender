class iCPEModel(db.Model):
    '''
    iCPE attached to a Node
    '''
    __tablename__ = 'icpe'
    id = db.Column(db.Integer, primary_key=True)
    mac = db.Column(db.String(12), unique=True)
    alias = db.Column(db.String(20), unique=True)
    created_on = db.Column(db.DateTime)
    online =  db.Column(db.Boolean)
    last_online = db.Column(db.DateTime)
    znodes = db.relationship('NodeModel', backref='icpe')
    events = db.relationship('NodeEventModel', backref='icpe')
    heat = db.relationship('NodeHeatModel', backref='icpe')
    power = db.relationship('NodePowerModel', backref='icpe')
    heatstat = db.relationship('NodeHeatStatModel', backref='icpe')
    powerstat = db.relationship('NodePowerStatModel', backref='icpe')
    notes = db.relationship('NodeNotesModel', backref='icpe')
    notesticky = db.Column(db.String(150))

    def __init__(self, mac, alias):
        self.mac = mac.upper()
        self.alias = alias.capitalize()
        self.created_on = datetime.now()
        logger.info('iCPE {} succesfully added'.format(self.mac))

    def __repr__(self):
        return '<Node %r, Mac %r>' % (self.alias, self.mac)


class ZWaveDeviceModel(db.Model):
    '''
    ZWave Node, child of iCPE
    '''
    # Table storing Zwave nodes on iCPE Nodes
    __tablename__ = 'zwavedevice'
    id = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(20))
    parent_id = db.Column(db.Integer, db.ForeignKey('icpe.id'))
    nodeid = db.Column(db.Integer)
    vid = db.Column(db.String(10))
    ptype = db.Column(db.String(10))
    pid = db.Column(db.String(10))
    generic_class = db.Column(db.String(10))
    productname = db.Column(db.String(30))
    brandname = db.Column(db.String(30))
    nodeclasses = db.relationship('NodeClassModel', backref='node')

    def __init__(self, nodeid, vid, ptype, pid, generic_class, productname,
                 brandname):
        self.alias = productname
        self.nodeid = nodeid
        self.vid = vid
        self.ptype = ptype
        self.pid = pid
        self.generic_class = generic_class
        self.productname = productname
        self.brandname = brandname

class ZWaveClassModel(db.Model):
    __tablename__ = 'zwavelass'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('node.id'))
    parent = db.relationship('NodeModel', backref='NodeClasses')
    commandclass = db.Column(db.String(10))
    hiddenFields = db.relationship('NodeHiddenFieldModel', backref='NodeClasses')

    def __init__(self, commandclass):
        self.commandclass = commandclass

class ZWaveHiddenFieldModel(db.Model):
    __tablename__ = 'zwavehiddenfields'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('nodeclass.id'))
    field = db.Column(db.String(10))

    def __init__(self, field):
        self.field = field
