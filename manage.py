#!./py/bin/python
from flask_script import Manager, Command
from NodeDefender import app, db
from flask_migrate import Migrate, MigrateCommand
from NodeDefender.manage.user import CreateUserCommand, DeleteUserCommand, \
ListUserCommand
from NodeDefender.manage.role import AddRole, CreateRole
from NodeDefender.manage.group import CreateGroupCommand, \
        AddUserCommand, ListGroupCommand, ListMemberCommand

manager = Manager(app)
manager.add_command('create_user', CreateUserCommand())
manager.add_command('delete_user', DeleteUserCommand())
manager.add_command('list_users', ListUserCommand())

manager.add_command('add_role', AddRole())
manager.add_command('create_role', CreateRole())

manager.add_command('create_group', CreateGroupCommand())
manager.add_command('add_user', AddUserCommand())
manager.add_command('list_groups', ListGroupCommand())
manager.add_command('list_members', ListMemberCommand())

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
