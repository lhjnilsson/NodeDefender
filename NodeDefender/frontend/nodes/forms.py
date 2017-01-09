from wtforms import StringField, BooleanField, SelectField, validators
from flask_wtf import Form

class SensorForm(Form):
    NodeField = StringField([validators.DataRequired()]);

class NodeLocationForm(Form):
    street = StringField("Steet", [validators.DataRequired()])
    city = StringField("City", [validators.DataRequired()])
    geolat = StringField("Latitude", [validators.DataRequired()])
    geolong = StringField("Longitude", [validators.DataRequired()])

class iCPEForm(Form):
    alias = StringField('Alias', [validators.InputRequired()])
    comment = StringField('Comment', validators=[])

class NodeForm(Form):
    alias = StringField('Alias', [validators.InputRequired()])

class NodeCreateForm(Form):
    Name = StringField('Name', [validators.DataRequired()])
    Group = StringField('Group', [validators.DataRequired()])
    Mac = StringField('Mac', [validators.DataRequired()])
    Street = StringField('Street', [validators.DataRequired()])
    City = StringField('City', [validators.DataRequired()])
