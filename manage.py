#!./py/bin/python
from flask_script import Manager, Command
from NodeDefender import app, db
from flask_migrate import Migrate, MigrateCommand

manager = Manager(app)



migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
