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


