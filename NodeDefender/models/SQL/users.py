from ... import db
from flask_security import UserMixin, RoleMixin

roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')))

class UserRoleModel(RoleMixin, db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __init__(self):
        pass



class UserModel(UserMixin, db.Model):
    '''
    Table of Users

    Users is a part of a Group
    Logins are logged with List- Relation(LoginLogModel)
    Private messages are stored in List- relation(UserMessageModel)

    Password is encrypted
    '''
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(30))
    lastname = db.Column(db.String(40))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(120))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime)
    last_login_at = db.Column(db.DateTime)
    current_login_at = db.Column(db.DateTime)
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)
    registered_at = db.Column(db.DateTime)

    roles = db.relationship('UserRoleModel', secondary=roles_users,
                            backref=db.backref('usersrole', lazy='dynamic'))
    messages = db.relationship('UserMessageModel', backref='user')


class UserMessageModel(db.Model):
    # Mailbox for User. 
    __tablename__ = 'usermessage'
    '''
    Message Inbox for User

    Author is who sent it
    uuid is to be able to present the message in secure manners
    subject is the topic of the message
    body is the body.
    created_on is when the message was sent from Author to User
    '''
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    author = db.relationship('UserModel', backref='usermessage')
    uuid = db.Column(db.String(40))
    subject = db.Column(db.String(50))
    body = db.Column(db.String(300))
    created_on = db.Column(db.DateTime)

    def __init__(self, author, subject, message):
        self.uuid = str(uuid4())
        self.subject = subject
        self.body = body
        self.created_on = datetime.now()
