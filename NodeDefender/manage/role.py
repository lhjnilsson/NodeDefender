from .. import UserDatastore, db
from ..models.manage import role
from flask_script import Manager, prompt

manager = Manager(usage="Administrate Roles")

@manager.option('-n', '-e', '--email', dest='email', default=None)
def technician(email):
    "List users that are member of a group"
    if email is None:
        email = prompt('Email of User')
    return role.technician(email)

@manager.option('-n', '-e', '--email', dest='email', default=None)
def admin(email):
    "List users that are member of a group"
    if email is None:
        email = prompt('Email of User')
    return role.admin(email)

@manager.option('-n', '-e', '--email', dest='email', default=None)
def superuser(email):
    "List users that are member of a group"
    if email is None:
        email = prompt('Email of User')
    return role.superuser(email)


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
