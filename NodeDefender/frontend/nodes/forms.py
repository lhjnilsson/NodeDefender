class NodeForm(Form):
    NodeField = StringField([validators.DataRequired()]);

class iCPEAddressForm(FlaskForm):
    street = StringField("Steet", [validators.DataRequired()])
    city = StringField("City", [validators.DataRequired()])
    geolat = StringField("Latitude", [validators.DataRequired()])
    geolong = StringField("Longitude", [validators.DataRequired()])

class iCPEBasicForm(FlaskForm):
    alias = StringField('Alias', validators=[InputRequired()])
    comment = StringField('Comment', validators=[])

class NodeBasicForm(FlaskForm):
    alias = StringField('Alias', validators=[InputRequired()])

