from .. import app

def production():
    app.config.from_object('factory.ProductionConfig')

def development():
    app.config.from_object('factory.DevelopmentConfig')

def testing():
    app.config.from_object('factory.TestingConfig')
