from .. import UserDatastore, db
from ..models.manage import role
from flask_script import Manager, prompt

manager = Manager(usage="Administrate Roles")

@manager.option('-n', '--name', dest='name', default=None)
@manager.option('-d', '--desc', dest='desc', default=None)
def create(name, desc):
    'Create Role'
    if name is None:
        name = prompt('Role Name')

    if desc is None:
        desc = prompt('Description')

    try:
        role.Create(name, desc)
    except ValueError:
        print("Role already present")
        return

    print("Role {} Successfully added!".format(name))

@manager.option('-i', '--index', dest='index', default=None)
@manager.option('-n', '--name', dest='name', default=None)
def delete(name, index):
    "Delete Role"
    if name is None and index is None:
        name = prompt("Index or Name")
    
    try:
        r = role.Delete((name if name else index))
    except LookupError:
        print("Unable to find Role")
        return

    print("Role {} Succesfully Removed".format(r.name))

@manager.option('-n', '--name', dest='name', default=None)
@manager.option('-i', '--index', dest='index', default=None)
def get(name, index):
    if name is None and index is None:
        name = prompt("Index or Name")
        
    r = role.Get((name if name else index))
    if r is None:
        print("Unable to find Node")
        return

    print("ID: {}, Name: {}".format(r.id, r.name))
    print("Description: {}".format(r.description))
    print("Users: ")
    for u in r.users:
        print("ID: {}, Email: {}".format(u.id, u.email))

@manager.command
def list():
    "List Avalible Roles"
    for r in role.List():
        print("ID: {}, Role: {}".format(r.id, r.name))

@manager.option('-n', '--name', dest='name', default=None)
def users(name):
    "List users that are member of a group"
    print("Members of Role: ", name)
    for user in role.Users(name):
        print("ID: {}, Email: {}".format(user.id, user.email))
