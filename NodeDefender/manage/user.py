from .. import app, UserDatastore, db
from flask_security import utils
from sys import exit
from flask_script import Command, prompt, prompt_pass
from ..models.manage import user
from flask_script import Manager

manager = Manager(usage="Preform User- operations in SQL Database")

@manager.option('-n', '-e', '--email', dest='email', default=None)
@manager.option('-pw', '--password', dest='password', default=None)
def create(email, password):
    if email is None:
        email = prompt('Email')

    if password is None:
        password = prompt_pass('Password')
    
    try:
        user.Create(email, password)
    except ValueError:
        print("User already present")
        return

    print("User {} Successfully added!".format(email))

@manager.command
def list():
    "List Users"
    for u in user.List():
        print("ID: {}, Email: {}".format(u.id, u.email))

@manager.option('-n', '-e', '--email', dest='email', default=None)
def delete(email):
    "Deltes User"
    if email is None:
        email = prompt('Email')

    user.Delete(email)
    print("User {} Successfully Deleted!".format(email))

@manager.option('-n', '-e', '--email', dest='email', default=None)
def groups(email):
    "List User Groups"
    if email is None:
        email = prompt('Email')
    for user in user.Groups:
        print("ID: {}, Email: {}".format(user.id, user.email))

@manager.option('-n', '-e', '--email', dest='email', default=None)
def roles(email):
    "List User Roles"
    if email is None:
        email = promot('Email')
    for role in user.Roles(email):
        print("ID: {}, Role: {}".format(role.id, role.name))
