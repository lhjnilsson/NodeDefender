from wtforms import StringField, BooleanField, SelectField, SubmitField, validators
from ...settings import ReadServer
from flask_wtf import FlaskForm as Form
def loggingchoices():
    '''
    utility for AdminServerForm
    '''
    for index, choice in enumerate(['debug', 'info', 'warning', 'error',
                                    'critical']):
        yield index, choice

def sqlchoices():
    '''
    utility for AdminServerForm
    '''
    for index, choice in enumerate(['local', 'mysql']):
        yield index, choice

def confparser(section, parameter):
    conf = ReadServer()
    return conf[section][parameter]

class GeneralForm(Form):
    Port = StringField('Server Port', [validators.DataRequired(
                        message='port')], default = confparser('BASE', 'port'))
    Debug = BooleanField('Debug Mode',[validators.DataRequired(\
                        message='debug')], default = eval(confparser('BASE', 'debug')))
    Logging = SelectField('Log Level',[validators.DataRequired(message='logging')]\
                          , default = confparser('BASE', 'logging'), \
                          choices = [(key, value) for key, value in loggingchoices()])
    SQLDriver = SelectField('SQL Driver',[validators.DataRequired(message='sqldriver')],\
                            default = confparser('BASE', 'sqldriver'),
                            choices = [(key, value) for key, value in sqlchoices()])
    Submit = SubmitField('Update')

class DatabaseServerForn(Form):
    SQL = StringField()
    TrackModifications = BooleanField()


class CreateUserForm(Form):
    Firstname = StringField('First name')
    Lastname = StringField('Last name')
    Email = StringField('Email')
    Submit = SubmitField('Create')

class CreateGroupForm(Form):
    Name = StringField('Group Name')
    Email = StringField('Email')
    Description = StringField('Description')
    Submit = SubmitField('Create')
