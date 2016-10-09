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
from wtforms import StringField, BooleanField, PasswordField, SelectField, Form, validators
from .chconf import *
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, InputRequired

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

class NodeForm(Form):
    NodeField = StringField([validators.DataRequired()]);

class LoginForm(Form):
    email = StringField('Email', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    remember_me = BooleanField('Remember me', default=False)

class RegisterForm(Form):
    firstname = StringField('Firstname', [validators.Length(min=1, max=30)])
    lastname = StringField('Lastname', [validators.Length(min=1, max=40)])
    email = StringField('Email', [validators.Length(min=5, max=50)])
    password = PasswordField('Password', [validators.DataRequired(),
                                              validators.EqualTo('confirm',
                                                                 message="Passwords must match")])
    confirm = PasswordField('Repeat')

class AdminServerForm(Form):
    port = StringField('Server Port',[validators.DataRequired(message='port')], default = confparser('BASE', 'port')
                       )
    debug = BooleanField('Debug Mode',[validators.DataRequired(message='debug')], default = eval(confparser('BASE',
                                                                 'debug'))
                         )
    logging = SelectField('Log Level',[validators.DataRequired(message='logging')], default = confparser('BASE', 'logging'),\
                          choices = [(key, value) for key, value in
                                     loggingchoices()]
                          )
    sqldriver = SelectField('SQL Driver',[validators.DataRequired(message='sqldriver')], default = confparser('BASE',
                                                               'sqldriver'),
                            choices = [(key, value) for key, value in
                                       sqlchoices()]
                            )

class DatabaseServerForn(Form):
    SQL = StringField()
    TrackModifications = BooleanField()

class NodeAddressForm(FlaskForm):
    street = StringField("Steet", [validators.DataRequired()])
    city = StringField("City", [validators.DataRequired()])
    geolat = StringField("Latitude", [validators.DataRequired()])
    geolong = StringField("Longitude", [validators.DataRequired()])

class NodeBasicForm(FlaskForm):
    alias = StringField('Alias', validators=[InputRequired()])
    comment = StringField('Comment', validators=[])
