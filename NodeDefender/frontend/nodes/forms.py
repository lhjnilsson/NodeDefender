from wtforms import Form, StringField, BooleanField, SelectField, validators

class NodeForm(Form):
    NodeField = StringField([validators.DataRequired()]);

class iCPEAddressForm(Form):
    street = StringField("Steet", [validators.DataRequired()])
    city = StringField("City", [validators.DataRequired()])
    geolat = StringField("Latitude", [validators.DataRequired()])
    geolong = StringField("Longitude", [validators.DataRequired()])

class iCPEBasicForm(Form):
    alias = StringField('Alias', [validators.InputRequired()])
    comment = StringField('Comment', validators=[])

class NodeBasicForm(Form):
    alias = StringField('Alias', [validators.InputRequired()])

