from .. import app, db
from flask_script import Command, prompt, prompt_pass
from ..models.manage import user
from flask_script import Manager

manager = Manager(usage="Preform User- operations in SQL Database")

@manager.option('-n', '-e', '--email', dest='email', default=None)
@manager.option('-pw', '--password', dest='password', default=None)
def create(email, password):
    'Create User Account'
    if email is None:
        email = prompt('Email')

    if password is None:
        password = prompt_pass('Password')
    
    try:
        user.Create(email)
        user.Password(email, password)
    except ValueError:
        print("User already present")
        return

    print("User {} Successfully added!".format(email))


@manager.option('-i', '--index', dest='index', default=None)
@manager.option('-n', '-e', '--email', dest='email', default=None)
def delete(email, index):
    "Deltes User"
    if email is None and index is None:
        email = prompt('Email or Index')

    try:
        u = user.Delete((email if email else index))
    except LookupError as e:
        print("Error: ", e)

    print("User {} Successfully Deleted!".format(u.email))

@manager.command
def list():
    "List Users"
    for u in user.List():
        print("ID: {}, Email: {}".format(u.id, u.email))

@manager.option('-n', '-e', '--email', dest='email', default=None)
def groups(email):
    "List User Groups"
    if email is None:
        email = prompt('Email')
    for g in user.Groups(email):
        print("ID: {}, Name: {}".format(g.id, g.name))

@manager.option('-n', '-e', '--email', dest='email', default=None)
@manager.option('-g', '--group', dest='group', default=None)
def join(email, group):
    'Add Group to User'
    if email is None:
        email = prompt('Email')
    if group is None:
        group = prompt('Group')

    try:
        user.Join(email, group)
    except LookupError as e:
        print("Error: ", e)
        return

    print("User {}, Successfully added to {}".format(email, group))

@manager.option('-n', '-e', '--email', dest='email', default=None)
@manager.option('-g', '--group', dest='group', default=None)
def leave(email, group):
    'Remove Role from User'
    if email is None:
        email = prompt('Email')
    if group is None:
        group = prompt('Group')
        
    try:
        user.Leave(email, group)
    except LookupError as e:
        print("Error: ", e)
        return

    print("User {}, Successfully removed from {}".format(email, group))

@manager.option('-n', '-e', '--email', dest='email', default=None)
def roles(email):
    "List User Roles"
    if email is None:
        email = prompt('Email')
    for r in user.Roles(email):
        print("ID: {}, Role: {}".format(r.id, r.name))

@manager.option('-n', '-e', '--email', dest='email', default=None)
@manager.option('-r', '--role', dest='role', default=None)
def add(email, role):
    'Add Role to User'
    if email is None:
        email = prompt('Email')
    if role is None:
        role = prompt('Role')

    try:
        user.Add(email, role)
    except LookupError as e:
        print("Error: ", e)
        return

    print("User {}, Successfully added to {}".format(email, role))

@manager.option('-n', '-e', '--email', dest='email', default=None)
@manager.option('-r', '--role', dest='role', default=None)
def remove(email, role):
    'Remove Role from User'
    if email is None:
        email = prompt('Email')
    if role is None:
        role = prompt('Role')

    try:
        user.Remove(email, role)
    except LookupError as e:
        print("Error: ", e)
        return

    print("User {}, Successfully removed from {}".format(email, role))
