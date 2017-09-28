from flask_script import Manager, prompt
import NodeDefender

manager = Manager(usage="Administrate Roles")

@manager.option('-n', '-e', '--email', dest='email', default=None)
def technician(email):
    "List users that are member of a group"
    if email is None:
        email = prompt('Email of User')
    return NodeDefender.db.user.set_role(email, 'technician')

@manager.option('-n', '-e', '--email', dest='email', default=None)
def admin(email):
    "List users that are member of a group"
    if email is None:
        email = prompt('Email of User')
    return NodeDefender.db.user.set_role(email, 'administrator')

@manager.option('-n', '-e', '--email', dest='email', default=None)
def superuser(email):
    "List users that are member of a group"
    if email is None:
        email = prompt('Email of User')
    return NodeDefender.db.user.set_role(email, 'superuser')


@manager.option('-n', '--name', dest='name', default=None)
@manager.option('-i', '--index', dest='index', default=None)
def get(name, index):
    if name is None and index is None:
        name = prompt("Index or Name")
        
    r = NodeDefender.db.user.Get((name if name else index))
    if r is None:
        print("Unable to find Node")
        return

    print("ID: {}, Name: {}".format(r.id, r.name))
    print("Description: {}".format(r.description))
    print("Users: ")
    for u in r.users:
        print("ID: {}, Email: {}".format(u.id, u.email))

