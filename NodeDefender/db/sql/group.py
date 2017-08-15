from NodeDefender.db.sql import SQL
from datetime import datetime
from NodeDefender.db.sql.node import LocationModel

user_list = SQL.Table('user_list',
                     SQL.Column('group_id', SQL.Integer,
                               SQL.ForeignKey('group.id')),
                     SQL.Column('user_id', SQL.Integer,
                               SQL.ForeignKey('user.id'))
                    )
node_list = SQL.Table('node_list',
                     SQL.Column('group_id', SQL.Integer,
                               SQL.ForeignKey('group.id')),
                     SQL.Column('node_id', SQL.Integer,
                               SQL.ForeignKey('node.id'))
                    )

mqtt_list = SQL.Table('mqtt_list',
                     SQL.Column('group_id', SQL.Integer,
                               SQL.ForeignKey('group.id')),
                     SQL.Column('mqtt_id', SQL.Integer,
                               SQL.ForeignKey('mqtt.id'))
                    )

class GroupModel(SQL.Model):
    '''
    Representing one group containing iCPEs and Users
    '''
    __tablename__ = 'group'
    id = SQL.Column(SQL.Integer, primary_key=True)
    name = SQL.Column(SQL.String(50))
    email = SQL.Column(SQL.String(120))
    description = SQL.Column(SQL.String(250))
    created_on = SQL.Column(SQL.DateTime)
    users = SQL.relationship('UserModel', secondary=user_list,
                            backref=SQL.backref('groups', lazy='dynamic'))
    mqtts = SQL.relationship('MQTTModel', secondary=mqtt_list,
                            backref=SQL.backref('groups', lazy='dynamic'))
    nodes = SQL.relationship('NodeModel', secondary=node_list,
                            backref=SQL.backref('groups', lazy='dynamic'))
    location = SQL.relationship('LocationModel', uselist=False,
                               backref='group')

    messages = SQL.relationship('MessageModel', backref='group',
                               cascade='save-update, merge, delete')

    def __init__(self, name, email, description):
        self.name = name
        self.email = email
        self.description = str(description)
        self.created_on = datetime.now()
    
    def to_json(self):
        return {'name' : self.name, 'email' : self.email, 'created' :
                str(self.created_on), 'description' : self.description,
                'users' : [user.email for user in self.users],
                'nodes' : [node.name for node in self.nodes]}
