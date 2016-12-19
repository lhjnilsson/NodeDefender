from wtforms import Form, StringField, BooleanField, PasswordField, SelectField, validators

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


