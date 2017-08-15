from NodeDefender import bcrypt
from NodeDefender.db.sql import SQL
from datetime import datetime

class UserModel(SQL.Model):
    '''
    Table of Users

    Users is a part of a Group
    Logins are logged with List- Relation(LoginLogModel)
    Private messages are stored in List- relation(UserMessageModel)

    Password is encrypted
    '''
    __tablename__ = 'user'
    id = SQL.Column(SQL.Integer, primary_key=True)
    firstname = SQL.Column(SQL.String(30))
    lastname = SQL.Column(SQL.String(40))
    email = SQL.Column(SQL.String(191), unique=True)
    password = SQL.Column(SQL.String(191))
    
    active = SQL.Column(SQL.Boolean())
    confirmed_at = SQL.Column(SQL.DateTime)
    registered_at = SQL.Column(SQL.DateTime)
    
    last_login_at = SQL.Column(SQL.DateTime)
    current_login_at = SQL.Column(SQL.DateTime)
    last_login_ip = SQL.Column(SQL.String(100))
    current_login_ip = SQL.Column(SQL.String(100))
    login_count = SQL.Column(SQL.Integer)
   
    technician = SQL.Column(SQL.Boolean)
    administrator = SQL.Column(SQL.Boolean)
    superuser = SQL.Column(SQL.Boolean)
    
    messages = SQL.relationship('MessageModel', backref='user',
                              cascade='save-update, merge, delete')

    def __init__(self, email):
        self.email = email
        self.firstname = None
        self.lastname = None
        self.password = None
        self.active = False
        self.confirmed_at = None
        self.registered_at = datetime.now()

        self.technician = False
        self.administrator = False
        self.superuser = False

    def to_json(self):
        return {'firstName': self.firstname,
                'lastName' : self.lastname,
                'email' : self.email,
               }

    def is_active(self):
        return True

    def get_id(self):
        return str(self.id)

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False

    def verify_password(self, password):
        if bcrypt.check_password_hash(self.password, password):
            return True
        else:
            return False
    

    def has_role(self, role):
        try:
            return getattr(self, role.lower())
        except AttributeError:
            print(role)
