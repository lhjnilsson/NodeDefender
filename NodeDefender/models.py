'''
Copyright (c) 2016 Connection Technology Systems Northern Europe

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE
SOFTWARE.
'''
from . import db, bcrypt, handler
from datetime import datetime
import logging
from uuid import uuid4
from geopy.geocoders import Nominatim

# Setup logging
logger = logging.getLogger('SQL')
logger.setLevel(logging.INFO)
logger.addHandler(handler)

'''

No idea why i cant have Major holder of all the Statitstics- tables...
somethings to work on later..

class Statistics(db.Model):
    __tablename__ = 'statistics'
    id = db.Column(db.Integer, primary_key=True)
    keyID = db.Column(db.Integer)
    hourly = db.relationship('HourlyStatistics', uselist=False,
                             backref="statistics")
    daily = db.relationship('DailyStatistics', uselist=False,
                            backref='statistics')
    weekly = db.relationship('WeeklyStatistics', uselist=False,
                             backref='statistics')
    dailylog = db.relationship('DailylogStatistics', backref='statistics')
    weeklylog = db.relationship('WeeklylogStatistics', backref='statistics')

    def __init__(self, keyID):
        self.keyID = keyID
'''
class HourlyStatistics(db.Model):
    __tablename__ = 'hourlystatistics'
    id = db.Column(db.Integer, primary_key=True)
    #parent_id = db.Column(db.Integer, db.ForeignKey('statistics.id'))
    heat = db.Column(db.Float)
    power = db.Column(db.Float)
    events = db.Column(db.Integer)
    last_updated = db.Column(db.DateTime)

    def __init__(self, heat, power, events):
        self.heat = heat
        self.power = power
        self.events = events
        last_updated = datetime.now()

class DailyStatistics(db.Model):
    __tablename__ = 'dailystatistics'
    id = db.Column(db.Integer, primary_key=True)
    #parent_id = db.Column(db.Integer, db.ForeginKey('statistics.id'))
    heat = db.Column(db.Float)
    power = db.Column(db.Float)
    events = db.Column(db.Integer)
    last_updated = db.Column(db.DateTime)

    def __init__(self, heat, power, events):
        self.heat = heat
        self.power = power
        self.events = events
        last_updated = datetime.now()

class WeeklyStatistics(db.Model):
    __tablename__ = 'weeklystatistics'
    id = db.Column(db.Integer, primary_key=True)
    #parent_id = db.Column(db.Integer, db.ForeginKey('statistics.id'))
    heat = db.Column(db.Float)
    power = db.Column(db.Float)
    events = db.Column(db.Integer)
    last_updated = db.Column(db.DateTime)

    def __init__(self, heat, power, events):
        self.heat = heat
        self.power = power
        self.events = events
        self.last_updated = datetime.now()

class HourlylogStatistics(db.Model):
    __tablename__ = 'hourlylogstatistics'
    id = db.Column(db.Integer, primary_key=True)
    heat = db.Column(db.Float)
    power = db.Column(db.Float)
    events = db.Column(db.Integer)
    last_updated = db.Column(db.DateTime)

    def __init__(self, heat, power, events):
        self.heat = heat
        self.power = power
        self.events = events
        self.last_updated = datetime.now()

class DailylogStatistics(db.Model):
    __tablename__ = 'dailylogstatistics'
    id = db.Column(db.Integer, primary_key=True)
    #parent_id = db.Column(db.Integer, db.ForeginKey('statistics.id'))
    heat = db.Column(db.Float)
    power = db.Column(db.Float)
    events = db.Column(db.Integer)
    last_updated = db.Column(db.DateTime)

    def __init__(self, heat, power, events):
        self.heat = heat
        self.power = power
        self.events = events
        self.last_updated = datetime.now()

class WeeklylogStatistics(db.Model):
    __tablename__ = 'weeklylogstatistics'
    id = db.Column(db.Integer, primary_key=True)
    #parent_id = db.Column(db.Integer, db.ForeginKey('statistics.id'))
    heat = db.Column(db.Float)
    power = db.Column(db.Float)
    events = db.Column(db.Integer)
    last_updated = db.Column(db.DateTime)

    def __init__(self, heat, power, events):
        self.heat = heat
        self.power = power
        self.events = events
        self.last_updated = datetime.now()


class UserModel(db.Model):
    '''
    Table of Users
    '''
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(30))
    lastname = db.Column(db.String(40))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(20))
    registered_on = db.Column(db.DateTime)
    last_login = db.Column(db.DateTime)
    messages = db.relationship('MessageModel', backref='user')
    loginlog = db.relationship('LoginLogModel', backref='user')

    # Permission level
    is_moderator = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.registered_on = datetime.now()
        logger.info('User {} added'.format(email))

    def is_authenticated(self):
        return True

    def verify_password(self, plaintext, ip):
        if bcrypt.check_password_hash(self.password, plaintext):
            logger.info('User: {} logged in from: {}'.format(self.email, ip))
            return True
        else:
            logger.warning('Unauthorized attempt for: {} from: {}'.format(self.email, ip))
            return False

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<Email: %r, Last Login: %r>' % (self.email, self.last_login)

class MessageModel(db.Model):
    # Mailbox for User. 
    __tablename__ = 'message'
    '''
    Message Inbox for User
    '''
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    uuid = db.Column(db.String(40))
    mailfrom = db.Column(db.String(50), default = "noreply@NodeDefender.com")
    subject = db.Column(db.String(50))
    body = db.Column(db.String(300))
    created_on = db.Column(db.DateTime)

    def __init__(self, subject, body):
        self.uuid = str(uuid4())
        self.subject = subject
        self.body = body
        self.created_on = datetime.now()


class LoginLogModel(db.Model):
    __tablename__ = 'loginlog'
    '''
    Loggs login for user, successful and unsuccessful
    '''
    id = db.Column(db.Integer, primary_key = True)
    parent_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.DateTime)
    successful = db.Column(db.Boolean)
    ipaddr = db.Column(db.String(48))
    browser = db.Column(db.String(16))
    platform = db.Column(db.String(16))

    def __init__(self, successful, ipaddr, user_agent):
        self.date = datetime.now()
        self.successful = successful
        self.ipaddr = ipaddr
        self.browser = user_agent.browser
        self.platform = user_agent.platform

class iCPEModel(db.Model):
    # Table storing iCPEs
    '''
    iCPEs
    '''
    __tablename__ = 'icpe'
    id = db.Column(db.Integer, primary_key=True)
    mac = db.Column(db.String(12), unique=True)
    alias = db.Column(db.String(20), unique=True)
    location = db.relationship('LocationModel', uselist=False,
                               backref='icpe')
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

    def __init__(self, mac, alias):
        self.mac = mac.upper()
        self.alias = alias.capitalize()
        self.created_on = datetime.now()
        logger.info('iCPE {} succesfully added'.format(self.mac))

    def __repr__(self):
        return '<Node %r, Mac %r>' % (self.alias, self.mac)

class LocationModel(db.Model):
    # Address of an iCPE
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

class NodeModel(db.Model):
    '''
    ZWave Node, child of iCPE
    '''
    # Table storing Zwave nodes on iCPE Nodes
    __tablename__ = 'node'
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

class NodeHeatStatModel(db.Model):
    __tablename__ = 'nodeheatstat'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('icpe.id'))
    parent = db.relationship('iCPEModel', backref='Heats')
    nodeid = db.Column(db.Integer)
    events = db.Column(db.Integer)
    heat = db.Column(db.Float)
    date = db.Column(db.DateTime)

    def __init__(self, nodeid, events, heat, date):
        self.nodeid = int(nodeid)
        self.events = int(events)
        self.heat = float(heat)
        self.date = date

class NodePowerStatModel(db.Model):
    __tablename__ = 'nodepowerstat'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('icpe.id'))
    parent = db.relationship('iCPEModel', backref='Powers')
    nodeid = db.Column(db.Integer)
    events = db.Column(db.Integer)
    power = db.Column(db.Float)
    date = db.Column(db.DateTime)

    def __init__(self, nodeid, events, power, date):
        self.nodeid = int(nodeid)
        self.events = int(events)
        self.power = float(power)
        self.date = date

class NodeEventModel(db.Model):
    '''
    ZWave event, child of iCPE
    '''
    __tablename__ = 'nodeevent'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('icpe.id'))
    parent = db.relationship('iCPEModel', backref='nodeevent')
    nodeid = db.Column(db.Integer)
    productname = db.Column(db.String(30))
    fonticon = db.Column(db.String(8))
    created_on = db.Column(db.DateTime)

    def __init__(self, nodeid, productname, fonticon):
        self.nodeid = int(nodeid)
        self.productname = productname
        self.fonticon = fonticon
        self.created_on = datetime.now()

class NodeHeatModel(db.Model):
    __tablename__ = 'nodeheat'
    '''
    Node Heat, child of iCPE
    '''
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('icpe.id'))
    parent = db.relationship('iCPEModel', backref='nodeheat')
    nodeid = db.Column(db.Integer)
    heat = db.Column(db.Float)
    unit = db.Column(db.String(10))
    fonticon = db.Column(db.String(8))
    created_on = db.Column(db.DateTime)

    def __init__(self, nodeid, heat, unit, fonticon):
        self.nodeid = int(nodeid)
        self.heat = heat
        self.unit = unit
        self.fonticon = fonticon
        self.created_on = datetime.now()

class NodePowerModel(db.Model):
    __tablename__ = 'nodepower'
    '''
    Node Power, child of iCPE
    '''
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('icpe.id'))
    parent = db.relationship('iCPEModel', backref='nodepower')
    nodeid = db.Column(db.Integer)
    power = db.Column(db.Float)
    unit = db.Column(db.String(10))
    fonticon = db.Column(db.String(8))
    created_on = db.Column(db.DateTime)

    def __init__(self, nodeid, power, unit, fonticon):
        self.nodeid = int(nodeid)
        self.power = power
        self.unit = unit
        self.fonticon = fonticon
        self.created_on = datetime.now()

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
