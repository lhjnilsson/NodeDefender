#!./py/bin/python
from flask_script import Manager, Command
from NodeDefender import app, db
from flask_migrate import Migrate, MigrateCommand
from NodeDefender.manage.user import manager as UserManager
from NodeDefender.manage.role import manager as RoleManager
from NodeDefender.manage.group import manager as GroupManager
from NodeDefender.manage.node import manager as NodeManager
from NodeDefender.manage.icpe import manager as iCPEManager
from NodeDefender.manage.sensor import manager as SensorManager
from NodeDefender.manage.mqtt import manager as MQTTManager
from NodeDefender.manage.setup import manager as SetupManager

manager = Manager(app)

manager.add_command('user', UserManager)
manager.add_command('role', RoleManager)
manager.add_command('group', GroupManager)
manager.add_command('node', NodeManager)
manager.add_command('iCPE', iCPEManager)
manager.add_command('sensor', SensorManager)
manager.add_command('mqtt', MQTTManager)
manager.add_command('setup', SetupManager)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
