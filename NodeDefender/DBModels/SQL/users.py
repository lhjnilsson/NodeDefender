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


