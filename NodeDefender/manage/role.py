from .. import UserDatastore, db
from ..models.manage import role
from flask_script import Manager, prompt

manager = Manager(usage="Administrate Roles")

@manager.option('-n', '--name', dest='name', default=None)
def create(name):
    if name is None:
        name = prompt('Role Name')

    try:
        role.Create(name)
    except DuplicateError:
        print("Role already present")
        return

    print("Role {} Successfully added!".format(role))

@manager.option('-n', '--name', dest='name', default=None)
def delete(name):
    "Delete Role"
    if name is None:
        name = prompt("Role name")
    
    try:
        role.Delete(name)
    except LookupError:
        print("Unable to find Role")

    print("Role {} Succesfully Removed".format(name))

@manager.command
def list():
    "List Avalible Roles"
    for role in role.List():
        print("ID: {}, Role: {}".format(role.id, role.name))


@manager.option('-n', '--name', dest='name', default=None)
def members(name):
    "List users that are member of a group"
    for users in role.Members(name):
        print("ID: {}, Email: {}".format(user.id, user.email))
